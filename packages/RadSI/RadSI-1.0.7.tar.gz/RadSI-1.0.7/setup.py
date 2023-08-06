# -*- coding: utf-8 -*-
"""
Setup for RadSI - The Radiation Source Inventory
Author: Matthew Durbin
Date: Tue July 07 2020
"""

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="RadSI",
    version="1.0.7",
    py_modules=["RadSI"],
    author="Matthew Durbin",
    author_email="mud370@psu.edu",
    description="A CLI radiation source inventory",
    entry_points={"console_scripts": ["RadSI=RadSI:main"]},
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=["setuptools", "pandas", "numpy", "fire", "matplotlib",],
    python_requires=">=3.5",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    url="https://github.com/matthewdurbin/RadSI",
)
