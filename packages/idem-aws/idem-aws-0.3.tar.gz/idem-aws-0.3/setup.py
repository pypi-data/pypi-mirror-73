#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import python libs
import json
import os
import shutil
from setuptools import setup, Command

NAME = "idem-aws"
PYNAME = "idem_aws"
DESC = "Idem language provider for AWS"

# Version info -- read without importing
_locals = {}
with open("{}/version.py".format(PYNAME)) as fp:
    exec(fp.read(), None, _locals)
VERSION = _locals["version"]
SETUP_DIRNAME = os.path.dirname(__file__)
if not SETUP_DIRNAME:
    SETUP_DIRNAME = os.getcwd()

with open("README.md", encoding="utf-8") as f:
    LONG_DESC = f.read()

with open("requirements.txt") as f:
    REQUIREMENTS = f.read().splitlines()

with open("requirements-extra.json", "r") as f:
    REQUIREMENTS_EXTRA = json.loads(f.read())
    full = set()
    for li in REQUIREMENTS_EXTRA.values():
        full.update(set(li))
    REQUIREMENTS_EXTRA["FULL"] = full


class Clean(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        for subdir in (PYNAME, "tests"):
            for root, dirs, files in os.walk(
                os.path.join(os.path.dirname(__file__), subdir)
            ):
                for dir_ in dirs:
                    if dir_ == "__pycache__":
                        shutil.rmtree(os.path.join(root, dir_))


def discover_packages():
    modules = []
    for package in (PYNAME,):
        for root, _, files in os.walk(os.path.join(SETUP_DIRNAME, package)):
            pdir = os.path.relpath(root, SETUP_DIRNAME)
            modname = pdir.replace(os.sep, ".")
            modules.append(modname)
    return modules


setup(
    name=NAME,
    author="EITR Technologies, LLC",
    author_email="devops@eitr.tech",
    url="https://gitlab.com/saltstack/pop/idem-aws",
    version=VERSION,
    install_requires=REQUIREMENTS,
    extras_require=REQUIREMENTS_EXTRA,
    description=DESC,
    long_description=LONG_DESC,
    long_description_content_type="text/markdown",
    python_requires=">=3.6",
    classifiers=[
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Development Status :: 5 - Production/Stable",
    ],
    packages=discover_packages(),
    cmdclass={"clean": Clean},
)
