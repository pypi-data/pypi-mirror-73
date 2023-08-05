#!/usr/bin/python3
from setuptools import setup
import config

setup(
    name='typeguarder',
    version=config.__version__,
    packages=['typecheck'],
    author=config.__author__,
    description='Useful module for runtime type checking',
    setup_requires=['wheel'],
    url='https://github.com/m00ga/typecheck',
)
