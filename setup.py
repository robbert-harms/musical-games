#!/usr/bin/env python
# -*- coding: utf-8 -*-
import glob
import re
from setuptools import setup, find_packages


def load_requirements(fname):
    is_comment = re.compile("^\s*(#|--).*").match
    with open(fname) as fo:
        return [line.strip() for line in fo if not is_comment(line) and line.strip()]

with open("README.rst", "rt") as f: readme = f.read()
with open("docs/history.rst", "rt") as f: history = f.read().replace(".. :changelog:", "")
with open("musical_games/__init__.py") as f: version_file_contents = f.read()

requirements = load_requirements("requirements.txt")
requirements_tests = load_requirements("requirements_tests.txt")

ver_dic = {}
exec(compile(version_file_contents, "musical_games/__init__.py", "exec"), ver_dic)

setup(
    name="musical_games",
    version=ver_dic["VERSION"],
    description="Base classes for musical games in Python",
    long_description=readme + "\n\n" + history,
    author="Robbert Harms",
    author_email="robbert@xkls.nl",
    url="https://github.com/robbert-harms/musical-games",
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    license="LGPL v3",
    zip_safe=False,
    keywords="musical games, dice games, music, computer generated",
    classifiers=[
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Topic :: Scientific/Engineering"
    ],
    test_suite="tests",
    tests_require=requirements_tests,
    scripts=glob.glob('bin/mg-*')
)
