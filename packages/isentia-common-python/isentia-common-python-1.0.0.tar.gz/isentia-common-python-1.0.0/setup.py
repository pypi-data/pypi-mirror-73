from pathlib import Path

from setuptools import find_packages, setup

from isentia_common.__version__ import __version__


def long_description():
    filepath = Path(__file__).with_name("README.md")
    with open(filepath) as fd:
        return fd.read()


def requirements():
    filepath = Path(__file__).with_name("requirements.txt")
    with open(filepath) as fd:
        return fd.readlines()


setup(
    name="isentia-common-python",
    author="Isentia",
    version=__version__,
    python_requires=">=3.7",
    long_description=long_description(),
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=("tests",)),
    download_url="",
    install_requires=requirements(),
    summary="Isentia's Python library with useful common utilities",
)
