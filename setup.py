# This file is part of the myenv project
# https://github.com/mbarkhau/myenv
#
# (C) 2018 Manuel Barkhau (mbarkhau@gmail.com)
# SPDX-License-Identifier: MIT

import pathlib
import setuptools


def project_path(filename):
    return (pathlib.Path(__file__).parent / filename).absolute()


def read(filename):
    with project_path(filename).open(mode="r") as fh:
        return fh.read()


long_description = read("README.rst") + "\n\n" + read("CHANGELOG.rst")


setuptools.setup(
    name="myenv",
    license="MIT",
    author="Manuel Barkhau",
    author_email="mbarkhau@gmail.com",
    url="https://github.com/mbarkhau/myenv",
    version="201809.2b0",

    keywords="environ variables mypy config configuration",
    description="Environment Variable Parsing with Types",
    long_description=long_description,
    long_description_content_type="text/x-rst",

    packages=["myenv"],
    package_dir={"": "src"},
    python_requires=">=3.6",
    zip_safe=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS :: MacOS X",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
