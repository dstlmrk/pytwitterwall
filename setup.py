#!/usr/bin/env python3.4
# coding=utf-8

from setuptools import setup

with open('README.md') as f:
    long_description = ''.join(f.readlines())

setup(
    name='pytwitterwall',
    version='0.3.5',
    description='Simple program which reads posts from Twitter via its API.',
    long_description=long_description,
    author='Marek Dostál',
    author_email='dostam12@fit.cvut.cz',
    keywords='twitter,flask,api',
    license='Public Domain',
    url='https://github.com/dstlmrk/pytwitterwall',
    packages=['pytwitterwall'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: Public Domain',
        'Framework :: Flask',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Libraries',
    ],
    install_requires=['Flask', 'click>=6', 'Jinja2', 'requests'],
    entry_points={
        'console_scripts': [
            'pytwitterwall = pytwitterwall.run:main',
        ],
    },
    package_data={
        'pytwitterwall': [
            'static/bootstrap.min.css',
            'templates/pytwitterwall.html'
        ]
    },
    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'betamax', 'flexmock'],
)
