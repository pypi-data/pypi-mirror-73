#! python3
# -*- coding: utf-8 -*-

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tools-d1zcord",
    version="0.0.1",
    author="Stroganov Pavel Stanislavovich",
    author_email="pdizreq@gmail.com",
    description="Miscellaneous tools for everyday work",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fdzuJ/tools",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
