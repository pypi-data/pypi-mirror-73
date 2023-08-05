#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from glob import glob
from os.path import basename

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='calcifer_pde',
    version='0.1.1',
    description='Python Poisson solver on curvilinear 2-D grid',
    long_description=readme,
    long_description_content_type="text/markdown",
    keywords=["PDE", "temperature", "solver", "poisson", "curvilinear grid"],
    author='COOP',
    author_email='coop@cerfacs.fr',
    url='',
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    #license=license,
    packages=find_packages("src"),
    package_dir={"": "src"},
    py_modules=[path.splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    install_requires=[
        "numpy",
        "scipy",
        "arnica"
    ]
)
