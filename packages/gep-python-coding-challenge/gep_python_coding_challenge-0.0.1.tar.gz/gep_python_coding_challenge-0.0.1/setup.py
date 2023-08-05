#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function

from glob import glob
from os.path import basename
from os.path import splitext

from setuptools import find_packages
from setuptools import setup

def read():
    with open("README.md", "r") as f:
        return f.read()


setup(
    name='gep_python_coding_challenge',
    version='0.0.1',
    license='MIT',
    description='This package contains the beginner level assignments of the GEP Python Coding Challenge.',
    long_description=read(),
    long_description_content_type="text/markdown",
    author='JcS',
    author_email='joyce@hey.com',
    url='https://github.com/Joyce-NL/gep-python-coding-challenge',
    py_modules=['Problem01', 'Problem02', 'Problem41'],
    package_dir={'': 'src'},
    zip_safe=False,
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Other/Nonlisted Topic',
    ],
    keywords=[
        'Euler', 'Project Euler'
    ],
    python_requires='>=3.0',
    install_requires=[],
    extras_require={},
)
