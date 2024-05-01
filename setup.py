# -*- coding: utf-8 -*-
"""
Created on Sat Sep  9 18:31:31 2023

@author: Anton Baranikov
"""

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

setup(
    name='Budget tool',
    version='0.1.0',
    description='Tool to track expenses and income',
    long_description=readme,
    author='Anton Baranikov',
    author_email='baranikov90210@gmail.com',
    url='https://github.com/baronett90210/Budget_tool',
    packages=find_packages()
)