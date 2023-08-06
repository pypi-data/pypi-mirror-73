#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import setuptools
version = '0.0.1'

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(name='spfwhitelister',
    packages=['spfwhitelister'],
    entry_points={
        'console_scripts': [
            'spfwhitelister = spfwhitelister.__main__:main'
        ]
    },
    #packages=setuptools.find_packages(),
    version=version,
    author='François Wautier',
    author_email='francois@wautier.eu',
    description='Library/utility to maintain a list of while listed domains.',
    long_description=long_description,
    url='http://github.com/frawau/spfwhitelister',
    keywords = ["greylist","MTA"],
    license='MIT',
    install_requires=[
    "dnspython"
    ],
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
    ],
    zip_safe=False)
