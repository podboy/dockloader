# coding=utf-8

from setuptools import find_packages
from setuptools import setup

from dockloader.attribute import __author__
from dockloader.attribute import __author_email__
from dockloader.attribute import __description__
from dockloader.attribute import __project__
from dockloader.attribute import __url_bugs__
from dockloader.attribute import __url_code__
from dockloader.attribute import __url_docs__
from dockloader.attribute import __url_home__
from dockloader.attribute import __version__


def all_requirements():
    def read_requirements(path: str):
        with open(path, "r", encoding="utf-8") as rhdl:
            return rhdl.read().splitlines()

    requirements = read_requirements("requirements.txt")
    return requirements


setup(
    name=__project__,
    version=__version__,
    description=__description__,
    url=__url_home__,
    author=__author__,
    author_email=__author_email__,
    project_urls={"Source Code": __url_code__,
                  "Bug Tracker": __url_bugs__,
                  "Documentation": __url_docs__},
    packages=find_packages(include=["dockloader*"], exclude=["tests"]),
    install_requires=all_requirements())
