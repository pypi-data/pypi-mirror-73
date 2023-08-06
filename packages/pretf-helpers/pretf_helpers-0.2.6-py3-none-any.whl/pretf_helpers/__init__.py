# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from abc import ABCMeta, abstractmethod
from collections.abc import Iterable
from functools import partial
from pathlib import Path
from os import PathLike
from io import StringIO

from typing import Optional, Union, Tuple, Callable, Dict, List, Iterator

import ruamel.yaml as ryaml
from pretf.api import block, log


# region ##### Exceptions
class LabelConflict(RuntimeError):
    """Raised when an exact label has been defined in the same context"""

    pass


# endregion


# region ##### Helper functions & classes
PathEquiv = Union[str, Path, PathLike]
"""Workaround for PyCharm unable to recognize that Path is part of os.PathLike"""


def unwrap(s) -> str:
    """Removes the `${` and `}` wrappers around the returned identifier."""
    if not isinstance(s, str):
        s = str(s)
    if not s.startswith("${"):
        return s
    if not s.endswith("}"):
        return s
    return s[2:-1]


class DictAble(metaclass=ABCMeta):
    @abstractmethod
    def to_dict(self) -> dict:
        pass


class AttribDict(dict):
    """
    Implements a dict whose keys can be accessed like attributes.
    IMPORTANT: When invoking attribs with underscores, e.g. "like_this_one", if the key is not found in the
    underlying dict, this class will try looking for a key with the underscores replaced by dashes, "like-this-one".
    If you do not want this behavior, set the `._trydash` property to False after instantiation.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._trydash = True

    def __getattr__(self, name: str):
        if name in self:
            return self[name]
        if self._trydash:
            name_dashed = name.replace("_", "-")
            if name_dashed in self:
                return self[name_dashed]
        # All variants have been exhausted, let superclass handle the missing attrib
        return super().__getattribute__(name)

    @staticmethod
    def recursively_from_dict_(d: dict) -> "AttribDict":
        """
        Creates an AttribDict instance from a dict, recursively converting dict values into AttribDict objects.
        IMPORTANT NOTES:
        (1) Non-dict mutable values (e.g., list, set, etc.) will NOT be copied.
        (2) dicts inside mutable values (e.g., as an element of a list) will NOT be converted.

        :param d: dict object from which to create an AttribDict
        """
        rslt = AttribDict()
        for k, v in d.items():
            if isinstance(v, dict):
                rslt[k] = AttribDict.recursively_from_dict_(v)
            else:
                rslt[k] = v
        return rslt

    @staticmethod
    def from_yaml_(yaml_file: PathEquiv) -> "AttribDict":
        """
        Create an AttribDict instance from a YAML file, recursively converting dict values into AttribDict objects.
        See IMPORTANT NOTES on `recursively_from_dict_` staticmethod.

        :param yaml_file: path to the YAML file
        """
        if not yaml_file.exists():
            raise FileNotFoundError(f"File '{yaml_file}' not found!")
        with open(yaml_file, "rt") as fin:
            data = ryaml.safe_load(fin)
        if not isinstance(data, dict):
            raise ValueError(
                f"File '{yaml_file}' should have a dict as root object, but it doesn't!"
            )
        return AttribDict.recursively_from_dict_(data)


class InitScript:
    """
    Generates a uniform init-script to be used in an instance's first boot (e.g., AWS' "UserData" for
    EC2 instances.
    """

    def __init__(
        self,
        hostname: str = None,
        users_and_keys: Dict[str, List[str]] = None,
        interpreter: str = "/bin/bash",
    ):
        self.hostname = hostname
        self.users_and_keys = users_and_keys
        self.interpreter = interpreter

    def generate(self) -> str:
        with StringIO() as sio:
            sio.write(f"#!{self.interpreter}\n")
            sio.write(f"sudo hostnamectl set-hostname {self.hostname}\n")
            for user, keylist in self.users_and_keys.items():
                dotssh_dir = f"/home/{user}/.ssh"
                authkeys_file = f"{dotssh_dir}/authorized_keys"
                for key in keylist:
                    sio.write(f'printf "\\n%s\\n" "{key}" ')
                    sio.write(f">> /home/{user}/.ssh/authorized_keys\n")
                sio.write(f"chown {user}:{user} {authkeys_file}\n")
                sio.write(f"chmod -R 0600 {dotssh_dir} {dotssh_dir}/*\n")
            return sio.getvalue()


# endregion


# region ##### (Abstract) 'Private' Base Classes
class _SimpleBlock(Iterable):
    """
    Implements a simple block that does not have dependent/attached blocks.
    """

    def __init__(self, block_type: str, *labels: str):
        self._type = block_type
        self._labels = labels
        self._body = {}

    def __call__(self, **kwargs) -> "_SimpleBlock":
        self._body = kwargs
        return self

    def __iter__(self) -> Iterator[block]:
        yield self.block__

    def __getattr__(self, item):
        return getattr(self.block__, item)

    @property
    def block__(self) -> block:
        return block(self._type, *self._labels, self._body)

    @property
    def unwrapped__(self) -> str:
        return unwrap(self.block__)


class _CompoundResource(Iterable, metaclass=ABCMeta):
    """Prototypes a resource that has attached sub-resources."""

    def __init__(self, label1: str, label2: str):
        self._type = "resource"
        self._labels = (label1, label2)
        self._body = {}
        self._subres: Optional["_Collector"] = None

    # The @abstractmethod decorator forces subclasses to reimplement this dunder.
    # The reason being that sub-subclasses usually need to be able to invoke
    # super().__call__ ; if subclasses don't (re)implement __call__, then all
    # those sub-subclasses will fail.
    @abstractmethod
    def __call__(self, **kwargs) -> "_CompoundResource":
        self._body = kwargs
        return self

    @property
    def _resource(self) -> block:
        return block(self._type, *self._labels, self._body)

    def __getattr__(self, item):
        return getattr(self._resource, item)

    def __iter__(self) -> Iterator[block]:
        yield self._resource
        yield from self._subres


# noinspection PyNestedDecorators
class _Backend(Iterable, metaclass=ABCMeta):

    # These two ... 'constructs' are to implement "Abstract Class Properties"
    # Ref: https://stackoverflow.com/a/53417582/149900

    # noinspection PyPropertyDefinition
    @property
    @classmethod
    @abstractmethod
    def AcceptedArguments(cls) -> set:
        raise NotImplementedError

    # noinspection PyPropertyDefinition
    @property
    @classmethod
    @abstractmethod
    def ConfigAttribRemaps(cls) -> dict:
        raise NotImplementedError

    def __init__(self, **kwargs):
        unrecogs = [k for k in kwargs.keys() if k not in self.AcceptedArguments]
        if unrecogs:
            raise TypeError(f"Unrecognized arguments: {', '.join(unrecogs)}")
        self._cfg = kwargs
        self._renderer: Optional[Callable] = None

    @property
    @abstractmethod
    def type(self) -> str:
        pass

    @property
    @abstractmethod
    def remote_config(self) -> dict:
        pass

    def __iter__(self) -> block:
        yield self._renderer(**self._cfg)

    @classmethod
    def from_config_(cls, config):
        kwargs = dict(config)
        # noinspection PyUnresolvedReferences
        for orig, dest in cls.ConfigAttribRemaps.items():
            if orig not in kwargs:
                continue
            kwargs[dest] = kwargs.pop(orig)
        return cls(**kwargs)


class _Collector:
    def __init__(self):
        """
        Implements a collection -- with uniqueness -- whose members/elements can be restricted and/or preprocessed
        before getting collected.
        """
        self._coll = {}

        self._accepts: Union[DictAble, Tuple[DictAble, ...]] = ()
        """
        A type or tuple() of `types` that implements the `.to_dict()` method.
        """

        self._renderer: Optional[Callable[[str], Callable]] = None
        """
        self._renderer contains a function that accepts 1 arg "label"; this function must itself return
        a function that will be called with the actual body/config. Usually implemented like this:
        `partial(BlockGeneratingClass, "block_type")`
        """

    # noinspection PyMethodMayBeStatic
    def _element(self, value_dict: dict) -> dict:
        """Implements the builder/validator/injector for each config of the subres"""
        return value_dict

    def __setitem__(self, key, value):
        if key in self._coll:
            raise LabelConflict(f"Attempting to redefine element '{key}'")
        # noinspection PyTypeChecker
        if isinstance(value, self._accepts):
            value = value.to_dict()
        if not isinstance(value, dict):
            raise ValueError(f"Value must be instance of {self._accepts} or dict")
        self._coll[key] = self._element(value)

    def __iter__(self) -> Iterator[block]:
        yield from (
            self._renderer(label)(**element) for label, element in self._coll.items()
        )


class _Singleton(type):
    # Ref: https://stackoverflow.com/a/6798042/149900
    _Instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._Instances:
            cls._Instances[cls] = super().__call__(*args, **kwargs)
        return cls._Instances[cls]


# endregion


# region ##### SimpleBlock Classes
class Resource(_SimpleBlock):
    def __init__(self, res_type: str, label: str):
        super().__init__("resource", res_type, label)

    # Need to implement this or else subclasses of this won't be able to
    # do super().__call__()
    def __call__(self, **kwargs) -> "Resource":
        return super().__call__(**kwargs)


class Data(_SimpleBlock):
    def __init__(self, data_type: str, label: str):
        super().__init__("data", data_type, label)

    # Need to implement this or else subclasses of this won't be able to
    # do super().__call__()
    def __call__(self, **kwargs) -> "Data":
        return super().__call__(**kwargs)


# endregion


# region ##### Config system
class RemoteState(DictAble):
    def __init__(self, backend: str, config: dict):
        self.config = dict(backend=backend, config=config)

    def to_dict(self) -> dict:
        return self.config

    @classmethod
    def from_backend(cls, backend: _Backend) -> "RemoteState":
        return cls(backend=backend.type, config=backend.remote_config)


class _ConfigRemotes(_Collector):
    def __init__(self):
        super().__init__()
        self._accepts = RemoteState
        self._renderer: Callable = partial(Data, "terraform_remote_state")

    def __getattr__(self, item):
        return self._coll.get(item, self._renderer(item))

    def __setitem__(self, key, value):
        if key in self._coll:
            raise LabelConflict(f"Attempting to redefine element '{key}'")
        if isinstance(value, _Backend):
            value = RemoteState.from_backend(value)
        if isinstance(value, RemoteState):
            value = value.to_dict()
        if isinstance(value, dict):
            self._coll[key] = value
        else:
            raise TypeError(f"I don't know how to handle type {type(value)}")

    def outputs_(self, item, subitem):
        outputs = self._renderer(item).outputs
        return getattr(outputs, subitem)


class _ConfigClass(metaclass=_Singleton):
    def __init__(
        self,
        config_file: str = "config.yaml",
        secrets_file: str = "secrets.yaml",
        with_tf_recipe: bool = True,
    ):
        _cwd = Path.cwd()

        self._config_file: PathEquiv = _cwd / config_file
        try:
            self._cfg = AttribDict.from_yaml_(self._config_file)
        except FileNotFoundError:
            raise log.bad(f"Cannot find config file '{config_file}' in cwd")
        except ValueError:
            raise log.bad(
                f"Config file '{self._config_file}' should have been a dict, but it's not"
            )

        # Defer reading secrets file until actually needed,
        # because it is possible that we are not using it.
        self._secrets_file: PathEquiv = _cwd / secrets_file
        self._secrets = None

        self._default_tags = self._cfg.get("default_tags", {})
        if with_tf_recipe:
            self._default_tags["Terraform"] = _cwd.name

        self.remotes = _ConfigRemotes()

    def __getattr__(self, item: str):
        try:
            return getattr(self._cfg, item)
        except AttributeError:
            raise KeyError(f"Config item '{item}' not found!")

    def tags(self, **kwargs) -> dict:
        """
        Generates a dict for tags, derived (copied) from self._default_tags.
        Any non-None kwargs will update (add/replace) the derived dict.
        Any None kwargs will DELETE the same key (if exists) from the derived dict.

        :param kwargs: (Optional) Tags to add/replace/delete
        :return: Final set of tags
        """
        d = self._default_tags.copy()
        for k, v in kwargs.items():
            if v is None and k in d:
                del d[k]
            else:
                d[k] = v
        return d

    def __getitem__(self, item):
        return self._cfg[item]

    @property
    def SECRETS(self) -> AttribDict:
        if self._secrets is None:
            try:
                self._secrets = AttribDict.from_yaml_(self._secrets_file)
            except FileNotFoundError:
                raise log.bad(f"Cannot find secrets file '{self._secrets_file}' in cwd")
            except ValueError:
                raise log.bad(
                    f"Secrets file '{self._secrets_file}' should have been a dict, but it's not"
                )
        return self._secrets

    @SECRETS.setter
    def SECRETS(self, value: PathEquiv):
        self._secrets_file = value
        self._secrets = None

    def from_item_(self, config_item):
        if isinstance(config_item, AttribDict):
            pass
        elif isinstance(config_item, dict):
            config_item = AttribDict.recursively_from_dict_(config_item)
        elif isinstance(config_item, str):
            config_item = self[config_item]
        else:
            raise TypeError("config_item must be one of (AttribDict, dict, str)")
        return config_item


Config = _ConfigClass()

# endregion

# End of pretf_helpers/__init__.py
