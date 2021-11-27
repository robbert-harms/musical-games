#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import glob
from textwrap import dedent
import os
import sys
from setuptools import setup, find_packages, Command


def load_requirements(fname):
    is_comment = re.compile('^\s*(#|--).*').match
    with open(fname) as fo:
        return [line.strip() for line in fo if not is_comment(line) and line.strip()]


with open('README.rst', 'rt') as f:
    readme = f.read()

with open('musical_games/__version__.py') as f:
    version_file_contents = "\n".join(f.readlines())
    ver_dic = {}
    exec(compile(version_file_contents, "musical_games/__version__.py", 'exec'), ver_dic)


info_dict = dict(
    name="musical_games",
    version=ver_dic["VERSION"],
    description="Base classes for musical games in Python",
    long_description=readme,
    author="Robbert Harms",
    author_email="robbert@xkls.nl",
    url="https://github.com/robbert-harms/musical-games",
    packages=find_packages(),
    include_package_data=True,
    install_requires=load_requirements('requirements.txt'),
    license="LGPL v3",
    zip_safe=False,
    keywords="musical games, dice games, music, computer generated",
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.8',
        'Topic :: Scientific/Engineering'
    ],
    test_suite="tests",
    tests_require='requirements.txt',
    scripts=glob.glob('bin/mg-*')
)

setup(**info_dict)
