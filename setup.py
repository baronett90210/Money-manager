# -*- coding: utf-8 -*-
"""
Created on Sat Sep  9 18:31:31 2023

@author: Anton Baranikov
"""

from setuptools import setup, find_packages


setup(
    name='Budget tool',
    version='0.1.0',
    description='Tool to track expenses and income',
    author='Anton Baranikov',
    author_email='baranikov90210@gmail.com',
    url='https://github.com/baronett90210/Money-manager',
    packages=find_packages(),
    install_requires = [
       'pandas == 2.0.3',
       'numpy == 1.24.3',
       'matplotlib == 3.7.2'
   ]
)