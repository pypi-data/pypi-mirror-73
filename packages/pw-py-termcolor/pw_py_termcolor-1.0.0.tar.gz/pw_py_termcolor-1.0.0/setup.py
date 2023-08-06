#!/usr/bin/env python3
##~---------------------------------------------------------------------------##
##                        _      _                 _   _                      ##
##                    ___| |_ __| |_ __ ___   __ _| |_| |_                    ##
##                   / __| __/ _` | '_ ` _ \ / _` | __| __|                   ##
##                   \__ \ || (_| | | | | | | (_| | |_| |_                    ##
##                   |___/\__\__,_|_| |_| |_|\__,_|\__|\__|                   ##
##                                                                            ##
##  File      : setup.py                                                      ##
##  Project   : pw_py_termcolor                                               ##
##  Date      : Mar 25, 2020                                                  ##
##  License   : GPLv3                                                         ##
##  Author    : stdmatt <stdmatt@pixelwizards.io>                             ##
##  Copyright : stdmatt 2020                                                  ##
##                                                                            ##
##  Description :                                                             ##
##                                                                            ##
##---------------------------------------------------------------------------~##

import pathlib;
from setuptools import setup, find_packages;

SCRIPT_DIR = pathlib.Path(__file__).parent;
README     = (SCRIPT_DIR / "README.md").read_text();


setup(
    name="pw_py_termcolor",
version=    "1.0.0",
    keywords="terminal, ANSI, termcolors",

    description="coloring functions to ANSI terminals",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/stdmatt-libs/pw_py_termcolor",

    author="stdmatt",
    author_email="stdmatt@pixelwizards.io",

    packages=["pw_py_termcolor"],
    setup_requires=[""],

    license="GPLv3",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
        "Natural Language :: English",
    ],
)
