#! -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='kaddle',
    version='0.0.0',
    description='kaddle',
    long_description='kaddle',
    license='Apache License 2.0',
    url='https://github.com/bojone/bert4keras',
    author='bojone',
    author_email='bojone@spaces.ac.cn',
    install_requires=['paddlepaddle'],
    packages=find_packages()
)
