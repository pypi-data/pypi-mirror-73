#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
import sys

__VERSION__ = "0.2.3"

assert sys.version_info[0] == 3, "Uptick requires Python > 3"

setup(
    name="muptick",
    version=__VERSION__,
    description="Command line tool to interface with the Meta1 network",
    long_description=open("README.md").read(),
    download_url="https://github.com/xeroc/muptick/tarball/" + __VERSION__,
    author="Fabian Schuh",
    author_email="Fabian@chainsquad.com",
    maintainer="Fabian Schuh",
    maintainer_email="Fabian@chainsquad.com",
    url="http://muptick.rocks",
    keywords=["meta1", "library", "api", "rpc", "cli"],
    packages=["muptick", "muptick.apis"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
    ],
    entry_points={"console_scripts": ["muptick = muptick.cli:main"]},
    install_requires=open("requirements.txt").readlines(),
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    include_package_data=True,
)
