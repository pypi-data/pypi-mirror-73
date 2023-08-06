#!/usr/bin/env python

import os
import sys

from setuptools import setup, find_packages

__version__ = '2.1.0'

if sys.version_info < (3, 6):
    sys.exit('Error: tlr requires Python 3.6 or above')


def read(filename):
    """Read file contents."""
    return open(os.path.join(os.path.dirname(__file__), filename)).read()


setup(
    name='tlr',
    version=__version__,
    description=('VOGAMOS (Volcanic Gas Monitoring System) data acquisition '
                 'service library'),
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    license='MIT',
    install_requires=[
        'mysqlclient>=1.4.6',
        'python-decouple',
        'pytz',
        'sentry-sdk',
        'SQLAlchemy',
    ],
    author='Indra Rudianto',
    author_email='indrarudianto.official@gmail.com',
    url='https://gitlab.com/bpptkg/tlr',
    zip_safe=False,
    packages=find_packages(exclude=['docs', 'examples', 'tests']),
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Operating System :: POSIX :: Linux',
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ]
)
