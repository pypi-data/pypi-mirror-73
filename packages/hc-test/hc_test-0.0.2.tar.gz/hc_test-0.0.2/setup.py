#!/usr/bin/env python
# coding: utf-8

from setuptools import setup

setup(
    name='hc_test',
    version='0.0.2',
    author='handongzhe',
    author_email='robbinjackly@gmail.com',
    url='https://github.com/handongzhe/pypi_test',
    description=u'hc test pypi setup',
    packages=['hc_test'],
    install_requires=[],
    entry_points={
        'console_scripts': [
            'start=hc_test:hello_world',
            'test=hc_test:test'
        ]
    }
)
