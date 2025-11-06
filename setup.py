#!/usr/bin/python
# -*- coding: utf-8 -*-

from codecs import open
import os
from setuptools import setup


def read(*paths):
    """ read files """
    with open(os.path.join(*paths), "r", "utf-8") as filename:
        return filename.read()


setup(
    name="slack-cli",
    version="3.0.0",
    description="Slack CLI for productive developers",
    long_description=(read("README.rst")),
    url="https://github.com/regisb/slack-cli",
    install_requires=[
        "argcomplete",
        "appdirs<1.5",
        "slack_sdk>=3.37.0",
    ],
    extras_require={"development": ["black", "pylint"]},
    license="MIT",
    author="Régis Behmo",
    author_email="nospam@behmo.com",
    packages=["slackcli"],
    package_data={"slackcli": ["emoji.json"]},
    entry_points={"console_scripts": ["slack-cli=slackcli.cli:main"]},
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
)
