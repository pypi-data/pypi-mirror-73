#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup,find_packages

setup(
    name='higgsbacktest',
    version='0.1.0',
    description='My short description for my project.',

    author='instant2333',
    author_email='instant2333@gmail.com',
    python_requires='>=3.6.0',
    url= 'https://github.com/instant2333/Strategy',
    # py_modules=['StrategyBacktesting.CFSingleInstrumentStrategy',
    #           'StrategyBacktesting.GTASingleStockStrategy',
    #           'StrategyBacktesting.SingleInstrumentStrategy',],
    packages=['higgsbacktesting'],

    install_requires=[
        'numpy',
        'higgsboom',
        'pandas',
        'matplotlib',
    ],

    include_package_data=True,
    license='MIT',
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
)