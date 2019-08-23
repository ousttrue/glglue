#!/usr/bin/env python
# coding: utf-8

from setuptools import setup, find_packages
import sys
import glglue

setup(
    name='glglue',
    version=glglue.__version__,
    description='The glue code which mediates between OpenGL and some GUI',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
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
