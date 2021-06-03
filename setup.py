# -*- coding: utf-8 -*-

from setuptools import setup

setup(name="brick",
      version="0.1.0",
      install_requires=["click >= 8.0", "toml >= 0.9"],
      entry_points={"console_scripts": "bk = brick.cli:main"})
