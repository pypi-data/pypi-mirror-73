import setuptools

with open("README.md", "r") as fin:
    long_description = fin.read()

_gitlab_addr = "https://gitlab.com/pepoluan/pretf_helpers"

setuptools.setup(
    name="pretf_helpers",
    version="0.2.6",
    author="Pandu POLUAN",
    author_email="pepoluan@gmail.com",

    description="Helper functions and classes for the pretf package",
    keywords="terraform pretf provisioning cloud",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Build Tools",
        "Topic :: System :: Installation/Setup",
        "Topic :: System :: Systems Administration",
    ],

    url=_gitlab_addr,
    project_urls={
        "Bug Tracker": f"{_gitlab_addr}/-/issues",
        "Source Code": f"{_gitlab_addr}/-/tree/master",
        "Documentation": f"{_gitlab_addr}/-/wikis/home",
    },

    packages=setuptools.find_packages(),
    zip_safe=True,
    python_requires='>=3.6',
    install_requires=[
        "pretf", "pretf.aws", "configparser", "ruamel.yaml",
    ],
)
