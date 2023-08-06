#!/usr/bin/env python
"""
Setup script.
"""
import setuptools

from shuhari_toolkit import __version__
from shuhari_toolkit.fileutils import read_file_text


setuptools.setup(
    name="shuhari-toolkit",
    version=__version__,
    author="shuhari",
    author_email="shuhari@outlook.com",
    description="",
    long_description=read_file_text('README.md'),
    long_description_content_type="text/markdown",
    url="https://github.com/shuhari/shuhari-toolkit",
    packages=['shuhari_toolkit'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
