# coding: utf-8

try:
    import setuptools
    from setuptools import setup, find_packages
except ImportError:
    print("Please install setuptools.")

import os
long_description = 'A simple graphviz wrapper to visualize a graph like TensorFlow and TensorBoard'
if os.path.exists('README.rst'):
    long_description = open('README.rst').read()

setup(
    name  = 'tfgraphviz',
    version = '0.0.8',
    description = 'A visualization tool to show a graph like TensorFlow and TensorBoard',
    long_description = long_description,
    license = 'MIT',
    author = 'akimacho',
    author_email = 'kimura.akimasa@gmail.com',
    url = 'https://github.com/akimach/tfgraphviz',
    keywords = 'tensorflow tensor machine-learning graphviz ml deep-learning neural-network',
    packages = find_packages(),
    install_requires = ['graphviz'],
    classifiers = [
      'Programming Language :: Python :: 2.7',
      'Programming Language :: Python :: 3.3',
      'License :: OSI Approved :: MIT License',
      'Intended Audience :: Science/Research',
      'Intended Audience :: Education',
      'Topic :: Scientific/Engineering :: Mathematics',
    ]
)
