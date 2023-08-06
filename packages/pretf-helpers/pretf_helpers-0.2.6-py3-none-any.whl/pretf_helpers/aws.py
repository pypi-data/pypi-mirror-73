# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from abc import ABCMeta, abstractmethod
from functools import partial
from typing import Union, Optional, Dict, List, Sequence

from pretf.aws import provider_aws, terraform_backend_s3

from pretf_helpers import (
    Resource,
    Config,
    AttribDict,
    DictAble,
    Data,
    _Backend,
    _Collector,
    _CompoundResource,
)


# region ### AWS Helper Classes
class _AWS_HasRegion(metaclass=ABCMeta):
    @property
    @abstractmethod
    def region(self):
        return

    @region.setter
    @abstractmethod
    def region(self, value):
        pass


# endregion


# region ### AWS Provider & Backend
class AWS_ProviderConfig(_AWS_HasRegion):
    AcceptedArguments = {
        "alias",
        "access_key",
        "secret_key",
        "profile",
        "assume_role",
        "endpoints",
        "shared_credentials_file",
        "token",
        "max_retries",
        "allowed_account_ids",
        "forbidden_account_ids",
        "ignore_tags",
        "insecure",
        "skip_credentials_validation",
        "skip_get_ec2_platforms",
        "skip_region_validation",
        "skip_requesting_account_id",
        "skip_metadata_api_check",
        "s3_force_path_style",
    }
    DefaultRegion: str = None

    def __init__(self, version: str, region: str = None, **kwargs):
        self._args = {"version": version}
        unrecognizeds = []
        for k, v in kwargs.items():
            if k not in self.AcceptedArguments:
                unrecognizeds.append(k)
                continue
            self._args[k] = v
        if unrecognizeds:
            raise TypeError(f"Unknown arguments specified: {', '.join(unrecognizeds)}")
        self._args["region"] = region or self.DefaultRegion

    def __iter__(self):
        yield provider_aws(**self._args)

    @property
    def region(self):
        return self._args["region"]

    @region.setter
    def region(self, value):
        if value is None:
            self._args["region"] = self.DefaultRegion
        else:
            self._args["region"] = value


class AWS_Backend_S3(_Backend, _AWS_HasRegion):
    AcceptedArguments = {
        "endpoint",
        "encrypt",
        "acl",
        "access_key",
        "secret_key",
        "kms_key_id",
        "dynamodb_table",
        "profile",
        "shared_credentials_file",
        "token",
        "role_arn",
        "assume_role_policy",
        "external_id",
        "session_name",
        "workspace_key_prefix",
        "dynamodb_endpoint",
        "iam_endpoint",
        "sts_endpoint",
        "force_path_style",
        "skip_credentials_validation",
        "skip_metadata_api_check",
        "sse_customer_key",
        "max_retries",
    }
    ConfigAttribRemaps = {
        "tfstate": "key",
        "state_db": "dynamodb_table",
    }
    DefaultRegion: str = None

    def __init__(self, bucket: str, key: str, region: str = None, **kwargs):
        super().__init__(**kwargs)
        self.region = region
        self._cfg["bucket"] = bucket
        self._cfg["key"] = key
        self._renderer = terraform_backend_s3

    @property
    def type(self) -> str:
        return "s3"

    @property
    def remote_config(self) -> dict:
        return {
            "bucket": self._cfg["bucket"],
            "key": self._cfg["key"],
            "region": self.region,
        }

    @property
    def region(self):
        return self._cfg.get("region")

    @region.setter
    def region(self, value: str):
        if value is None:
            self._cfg["region"] = self.DefaultRegion
        else:
            self._cfg["region"] = value


# endregion


# region ### RDS Classes
class RDS_Parameter_Group(Resource):
    def __init__(self, label: str):
        super().__init__("aws_db_parameter_group", label)

    def __call__(
        self,
        family: str,
        tags: Optional[Dict[str, str]] = None,
        parameters: Optional[Union[list, dict]] = None,
        parameter: Optional[list] = None,
        **kwargs,
    ) -> "RDS_Parameter_Group":
        if parameter is None:
            parameter = []
        if parameters is not None:
            if isinstance(parameters, dict):
                parameter.extend({"name": k, "value": v} for k, v in parameters.items())
            elif isinstance(parameters, list):
                parameter.extend(parameters)
            else:
                raise TypeError("options must be dict or list")

        tags = tags or {}
        super().__call__(
            family=family, parameter=parameter, tags=Config.tags(**tags), **kwargs
        )
        return self

    def from_config_item_(
        self, config_item: Union[AttribDict, dict, str], tags: Optional[dict] = None
    ):
        config_item = Config.from_item_(config_item)
        tags = tags or {}
        return self(
            name=config_item.name,
            description=config_item.description,
            family=config_item.family,
            parameters=config_item.parameters,
            tags=tags,
        )


class RDS_Option_Group(Resource):
    def __init__(self, label: str):
        super().__init__("aws_db_option_group", label)

    def __call__(
        self,
        engine_name: str,
        major_engine_version: str,
        options: Optional[Union[list, Dict[str, str]]] = None,
        option: Optional[list] = None,
        tags: Optional[Dict[str, str]] = None,
        **kwargs,
    ) -> "RDS_Option_Group":
        if option is None:
            option = []
        if options is not None:
            if isinstance(options, dict):
                for opt_name, opt_setval in options.items():
                    for s_name, s_val in opt_setval.items():
                        option.append(
                            {
                                "option_name": opt_name,
                                "option_settings": {"name": s_name, "value": s_val},
                            }
                        )
            elif isinstance(options, list):
                raise NotImplementedError(
                    "Currently you can only specify options as dict"
                )
            else:
                raise TypeError("options must be dict or list")

        tags = tags or {}
        super().__call__(
            engine_name=engine_name,
            major_engine_version=major_engine_version,
            tags=Config.tags(**tags),
            option=option,
            **kwargs,
        )
        return self

    def from_config_item_(
        self, config_item: Union[AttribDict, dict, str], tags: Optional[dict] = None
    ):
        config_item = Config.from_item_(config_item)
        tags = tags or {}
        return self(
            name=config_item.name,
            option_group_description=config_item.description,
            engine_name=config_item.engine_name,
            major_engine_version=config_item.major_engine_version,
            options=config_item.get("options"),
            tags=tags,
        )


class RDS_Instance(Resource):
    CloudWatchLogsExports = ["error", "slowquery"]

    def __init__(self, label: str):
        super().__init__("aws_db_instance", label)

    def __call__(
        self,
        config_item,
        parameter_group: RDS_Parameter_Group,
        option_group: RDS_Option_Group,
        subnet_group_name,
        security_group_ids,
        username: str,
        password: str,
        **kwargs,
    ) -> "RDS_Instance":
        cfg = Config.from_item_(config_item)
        deps = [parameter_group.unwrapped__, option_group.unwrapped__]
        return super().__call__(
            depends_on=deps,
            identifier=cfg.identifier,
            multi_az=cfg.multi_az,
            db_subnet_group_name=subnet_group_name,
            vpc_security_group_ids=security_group_ids,
            instance_class=cfg.type,
            allocated_storage=cfg.storage_min_gb,
            max_allocated_storage=cfg.storage_max_gb,
            storage_type=cfg.storage_type,
            engine=cfg.engine,
            engine_version=cfg.engine_version,
            # parameter_group_name=parameter_group.block__.name,
            # option_group_name=option_group.block__.name,
            parameter_group_name=parameter_group.name,
            option_group_name=option_group.name,
            monitoring_interval=cfg.monitoring_interval,
            monitoring_role_arn=cfg.monitoring_role_arn,
            performance_insights_enabled=cfg.performance_insights,
            enabled_cloudwatch_logs_exports=self.CloudWatchLogsExports,
            backup_retention_period=cfg.backup_retention,
            backup_window=cfg.backup_window,
            copy_tags_to_snapshot=True,
            skip_final_snapshot=False,
            username=username,
            password=password,
            tags=Config.tags(Name=cfg.name),
        )


# endregion


# region ### LoadBalancer Classes
class LB_TargetGroup(Resource):
    def __init__(self, label: str):
        super().__init__("aws_lb_target_group", label)

    def __call__(
        self,
        *,
        name: str,
        port: Union[int, str],
        protocol: str,
        vpc_id,
        health_check_ports: Optional[str] = None,
        healthy_threshold: int = 5,
        unhealthy_threshold: int = 2,
    ) -> "LB_TargetGroup":
        kwargs = {
            "name": name,
            "port": port,
            "protocol": protocol,
            "vpc_id": vpc_id,
        }
        if health_check_ports == "disabled":
            kwargs["health_check"] = {"enabled": False}
        else:
            kwargs["health_check"] = {
                "enabled": True,
                "matcher": health_check_ports or "200",
                "healthy_threshold": healthy_threshold,
                "unhealthy_threshold": unhealthy_threshold,
            }
        return super().__call__(**kwargs)


class _LoadBalancerListeners(_Collector):
    def __init__(self, lb_arn):
        super().__init__()
        self.lb_arn = lb_arn
        self._renderer = partial(Resource, "aws_lb_listener")

    def _element(self, value_dict: dict) -> dict:
        return dict(**value_dict, load_balancer_arn=self.lb_arn)


class LoadBalancer(_CompoundResource):
    def __init__(self, label):
        super().__init__("aws_lb", label)

    def __call__(
        self,
        *,
        name: str,
        internal: bool,
        load_balancer_type: str,
        security_groups: list,
        subnets: list,
        enable_deletion_protection: bool,
        tags: Dict[str, str],
    ) -> "LoadBalancer":
        super().__call__(
            name=name,
            internal=internal,
            load_balancer_type=load_balancer_type,
            security_groups=security_groups,
            subnets=subnets,
            enable_deletion_protection=enable_deletion_protection,
            tags=tags,
        )
        self._subres = _LoadBalancerListeners(lb_arn=self._resource.arn)
        return self

    @property
    def listeners(self):
        return self._subres


# endregion


# region ### EC2 Classes
class EC2_AMI(Data):
    def __init__(self, label: str):
        super().__init__("aws_ami", label)

    def __call__(
        self,
        *,
        owners: Union[str, Sequence[str]],
        most_recent: bool = True,
        **filters: Union[str, Sequence[str]],
    ) -> "EC2_AMI":
        """
        Actually builds the "Data" block to get the AMI ID. The **filters will be marhalled into a format
        that Terraform expects.

        :param owners: A str containing AWS ID, or list of str containing AWS IDs
        :param most_recent: Whether to find only the most recent AMI
        :param filters: Keyword args representing the filter to be used in the search
        """
        owners: List[str] = [owners] if isinstance(owners, str) else list(owners)
        filter_list: List[Dict[str, Union[str, List[str]]]] = [
            {"name": k, "values": [v] if isinstance(v, str) else list(v)}
            for k, v in filters.items()
        ]
        return super().__call__(
            most_recent=most_recent, owners=owners, filter=filter_list,
        )


# endregion


# region ### SecurityGroup Classes
class SecurityGroupRule(DictAble):
    """Helper class to ensure that mandatory fields are provided when creating a Security Group Rule."""

    # noinspection PyShadowingBuiltins
    def __init__(
        self,
        type: str,
        from_port: int,
        to_port: int,
        protocol: Union[str, int],
        description: Optional[str] = None,
        **kwargs,
    ):
        self.config = dict(
            **kwargs, type=type, from_port=from_port, to_port=to_port, protocol=protocol
        )
        if description is not None:
            self.config["description"] = description

    def to_dict(self) -> Dict[str, Union[str, int]]:
        return self.config


class _SecurityGroupRules(_Collector):
    def __init__(self, sg_id):
        super().__init__()
        self.sg_id = sg_id
        self._accepts = SecurityGroupRule
        self._renderer = partial(Resource, "aws_security_group_rule")

    def _element(self, value_dict: dict) -> dict:
        return dict(**value_dict, security_group_id=self.sg_id)


class SecurityGroup(_CompoundResource):
    """Implements an AWS Security Group Resource, with subresources containing AWS Security Group Rule Resources"""

    ParentVPC = None

    def __init__(self, label):
        super().__init__("aws_security_group", label)

    def __call__(
        self, *, name, parent_vpc=None, description: str, tags: dict = None
    ) -> "SecurityGroup":
        super().__call__(
            name=name,
            description=description,
            vpc_id=(parent_vpc or self.__class__.ParentVPC).id,
            tags=tags,
        )
        self._subres = _SecurityGroupRules(sg_id=self._resource.id)
        return self

    @property
    def rules(self):
        return self._subres


# endregion


# End of pretf_helpers/aws.py
