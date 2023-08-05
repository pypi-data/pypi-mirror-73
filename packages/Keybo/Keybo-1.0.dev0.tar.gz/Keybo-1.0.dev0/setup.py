#!/usr/bin/python

from setuptools import setup

setup(
    name='Keybo',
    version='1.0.dev0',
    author='madmachinations',
    packages=['keybo'],
    license='LICENSE.txt',
    description='Useful towel-related stuff.',
    url='https://gitlab.com/keybo/',
    long_description=open('README.md').read(),
    namespace_packages=["keybo"],
    install_requires=[]
)