#!/usr/bin/env python
from setuptools import setup, find_packages

setup(name='sub2srt',
    version='0.1',
    description='Converts youtube transcript file into srt file',
    license='BSD',
    url='www.vxk.cz',
    author='vencax',
    author_email='vencax@centrum.cz',
    packages=find_packages(),
    install_requires=[],
    keywords="transcript srt",
    include_package_data=True,
)
