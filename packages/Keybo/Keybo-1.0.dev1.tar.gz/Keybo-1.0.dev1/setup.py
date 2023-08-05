#!/usr/bin/python

from setuptools import setup

setup(
    name='Keybo',
    version='1.0.dev1',
    author='madmachinations',
    packages=['keybo'],
    license='LICENSE.txt',
    description='A modular multi-platform bot designed to interconnect a company or project workflow',
    url='https://gitlab.com/keybo/',
    long_description=open('README.md').read(),
    namespace_packages=["keybo"],
    python_requires=">=3.6",
    install_requires=[]
)