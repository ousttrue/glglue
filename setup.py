#!/usr/bin/env python
# coding: utf-8

from setuptools import setup, find_packages
import sys

setup(
        name='glglue',
        version='0.1.2',
        description='The glue code which mediates between OpenGL and some GUI',
        long_description=open('README.rst').read(),
        classifiers=[
            'Programming Language :: Python :: 2',
            'License :: OSI Approved :: zlib/libpng License',
            'Topic :: Multimedia :: Graphics :: 3D Modeling',
            ],
        keywords=['opengl'],
        author='ousttrue',
        author_email='ousttrue@gmail.com',
        license='zlib',
        packages=find_packages(),
        test_suite='nose.collector',
        tests_require=['Nose'],
        )

