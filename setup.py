# coding: utf-8

try:
    import setuptools
    from setuptools import setup, find_packages
except ImportError:
    print("Please install setuptools.")

import os
long_description = 'Simple graphviz wrapper to visualize a graph like TensorBoard'
if os.path.exists('README.rst'):
    long_description = open('README.rst').read()

setup(
    name  = 'tfgraphviz',
    version = '0.0.1',
    description = 'Simple graphviz wrapper to visualize a graph like TensorBoard',
    long_description = long_description,
    license = 'MIT',
    author = 'akimacho',
    author_email = 'kimura.akimasa@gmail.com',
    url = 'https://github.com/akimach/tfgraphviz',
    keywords = 'tensorflow tensor machine learning graphviz',
    packages = find_packages(),
    install_requires = ['tensorflow', 'graphviz'],
    classifiers = [
      'Programming Language :: Python :: 2.7',
      'Programming Language :: Python :: 3.3',
      'License :: OSI Approved :: MIT License',
      'Intended Audience :: Science/Research',
      'Intended Audience :: Education',
      'Topic :: Scientific/Engineering :: Mathematics',
    ]
)