#!/usr/bin/python3

import codecs
import os
import re

from setuptools import setup, find_packages

long_description = """
Toolset for easy CI/CD integration
"""

requires = []

__name__ = 'integrator'
__description__ = "Ease the CI/CD integration"
__author__ = "Pavel Raiskup"
__author_email__ = "praiskup@redhat.com"
__url__ = "https://pagure.io/copr/copr"


setup(
    name=__name__,
    version="0.0.dev",
    description=__description__,
    long_description=long_description,
    author=__author__,
    author_email=__author_email__,
    url=__url__,
    license='GPLv2+',
    install_requires=requires,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)
