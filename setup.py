#!/usr/bin/env python
# coding: utf-8

from setuptools import setup
import sys
import os
import shutil

name='glglue'
version='0.0.8'
short_description='The glue code which mediates between OpenGL and some GUI'
long_description=open('README.rst').read()

classifiers=[
        'Programming Language :: Python :: 2',
        'License :: OSI Approved :: zlib/libpng License',
        'Topic :: Multimedia :: Graphics :: 3D Modeling',
        ]

setup(
        name=name,
        version=version,
        description=short_description,
        long_description=long_description,
        classifiers=classifiers,
        keywords=['opengl'],
        author='ousttrue',
        author_email='ousttrue@gmail.com',
        license='zlib',
        packages=['glglue', 'glglue.sample',],
        test_suite='nose.collector',
        tests_require=['Nose'],
        zip_safe = (sys.version>="2.5"),   # <2.5 needs unzipped for -m to work
        )

