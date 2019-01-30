import os
import sys

from setuptools import setup

setup(
    name='DigitalClass',
    version='0.1_beta',
    long_description=__doc__,
    packages=['noten'],
    include_package_data=True,
    zip_safe=False,
    install_requires=['Flask']
)