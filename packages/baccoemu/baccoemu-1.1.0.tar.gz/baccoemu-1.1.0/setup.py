#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import re

try:
    from setuptools import setup, Extension, sysconfig
    setup
except ImportError:
    from distutils.core import setup, Extension
    from distutils import sysconfig
    setup

with open("README.md", "r") as fh:
    long_description = fh.read()

import re
VERSIONFILE="baccoemu/_version.py"
verstrline = open(VERSIONFILE, "rt").read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, verstrline, re.M)
if mo:
    verstr = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))

setup(
    name="baccoemu",
    author="Raul E Angulo",
    author_email="rangulo@dipc.org",
    version=verstr,
    description="Dark matter power spectrum emulator",
    url="http://dipc.org/bacco/",
    license="MIT",
    packages=['baccoemu'],
    package_data={
        "baccoemu": ["LICENSE", "AUTHORS.rst"],
        "": ["*.pkl"]
    },
    include_package_data=True,
    install_requires=["numpy", "sklearn", "GPy", "keras",  "matplotlib", "scipy",
                      "tensorflow", "camb", "setuptools", "requests", "progressbar2"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ],
    python_requires='>=3.6',
)
