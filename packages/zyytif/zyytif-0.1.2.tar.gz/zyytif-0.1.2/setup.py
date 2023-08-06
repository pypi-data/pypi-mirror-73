#Author: Franklin
#Date: 7/10/2020
#Decription: 

from __future__ import print_function
from zyytif import *
from setuptools import setup, find_packages
import sys

setup(
    name='zyytif',
    version='0.1.2',
    description='Scientific computing for TIF',
    author='Franklin',
    author_email='franklinzhang@foxmail.com',
    maintainer='Franklin',
    maintainer_email='franklinzhang@foxmail.com',
    license='MIT License',
    packages=find_packages(),
    platforms=["all"],
    classifiers=[
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries'
    ],
    install_requires=[
        'GDAL', 
        'numpy'
    ],
    zip_safe=True
)