#!/usr/bin/env python

"""
Setuptools configuration
"""

import sys

if sys.version_info < (3, 5, 0):
    sys.stderr.write("ERROR: Python 3.5 or later is required.\n")
    exit(1)

from pathlib import Path  # noqa
from setuptools import setup, find_packages  # noqa

sys.path.insert(0, "src")

from twistedstyle import __version__ as version_string  # noqa


#
# Options
#

name = "twistedstyle"
description = "Flake8 plugin for Twisted code style"

readme_path = Path(__file__).parent / "README.rst"
try:
    long_description = readme_path.open().read()
except IOError:
    long_description = None

url = "https://github.com/wsanchez/twistedstyle"

author = "Wilfredo S\xe1nchez Vega"

author_email = "wsanchez@wsanchez.net"

license = ""

platforms = ["all"]

packages = find_packages(where="src")

classifiers = [
    "Framework :: Twisted",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3",
]


#
# Entry points
#

entry_points = {
    "console_scripts": [],
    "flake8.extension": [
        "t = twistedstyle.Flake8Plugin",
    ],
}


#
# Dependencies
#

setup_requirements = []

install_requirements = [
    "flake8>=3",
]

extras_requirements = {}


#
# Set up Extension modules that need to be built
#

extensions = []


#
# Run setup
#

def main():
    """
    Run :func:`setup`.
    """
    setup(
        name=name,
        version=version_string,
        description=description,
        long_description=long_description,
        url=url,
        classifiers=classifiers,
        author=author,
        author_email=author_email,
        license=license,
        platforms=platforms,
        packages=packages,
        package_dir={"": "src"},
        package_data={},
        entry_points=entry_points,
        scripts=[],
        data_files=[],
        ext_modules=extensions,
        py_modules=[],
        setup_requires=setup_requirements,
        install_requires=install_requirements,
        extras_require=extras_requirements,
    )


#
# Main
#

if __name__ == "__main__":
    main()
