# coding: utf-8

"""
    pychronos

    client for ChronosDB

    Contact: support@chronosdb.io

"""

from setuptools import find_packages  # , setup
from distutils.core import setup


NAME = "pychronos"
VERSION = "0.1.0"
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = ["urllib3 >= 1.15", "six >= 1.10", "certifi", "python-dateutil", "pandas", "bson >= 0.5.9", "PyYAML >= 5.3"]


setup(
    name=NAME,
    version=VERSION,
    license="Other/Proprietary License",
    description="Python client for ChronosDB, financial/economic/scientific/business time series database.",
    author_email="support@chronosdb.io",
    url="https://www.chronosdb.io/",
    download_url=f"https://www.pypi.org/project/pychronos/{VERSION}/",
    keywords=["pychronos", "ChronosDB", 'time series', 'database'],
    install_requires=REQUIRES,
    packages=find_packages(),
    include_package_data=True,
    long_description="""\
    Python client for ChronosDB, financial/economic/scientific/business time series database.
    """,
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python :: 3",
        "Topic :: Database :: Front-Ends",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Intended Audience :: Financial and Insurance Industry",
        "Intended Audience :: Science/Research",
    ]
)
