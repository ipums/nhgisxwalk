# This file is part of the Minnesota Population Center's NHGISXWALK.
# For copyright and licensing information, see the NOTICE and LICENSE files
# in this project's top-level directory, and also on-line at:
#   https://github.com/ipums/nhgisxwalk

import os
import sys

import versioneer
from setuptools import setup

# ensure the current directory is on sys.path so versioneer can be imported
# when pip uses PEP 517/518 build rules.
# https://github.com/python-versioneer/python-versioneer/issues/193
sys.path.append(os.path.dirname(__file__))

# see pyproject.toml for static project metadata
setup(version=versioneer.get_version(), cmdclass=versioneer.get_cmdclass())
