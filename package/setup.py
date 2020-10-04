#!/usr/bin/env python3
import setuptools

with open("../README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="pyorganalyze-oakrc",
    version="0.0.1",
    author="Zhenkai Weng",
    author_email="oakrc@protonmail.com",
    description="Org-mode clocks analysis tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/oakrc/pyorganalyze",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha"
        "Topic :: Text Editors :: Emacs"
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
