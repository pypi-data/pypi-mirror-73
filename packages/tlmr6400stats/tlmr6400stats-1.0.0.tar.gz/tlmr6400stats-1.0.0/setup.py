# coding: utf-8
from setuptools import setup, find_packages  # noqa: H301

NAME = "tlmr6400stats"
VERSION = "1.0.0"
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = [
    'requests', 'influxdb', 'urllib3'
]

setup(
    name=NAME,
    version=VERSION,
    description="Tool to read stats from TL-MR6400 LTE router and push these to influxdb",
    author_email="ssch@wheel.dk",
    url="",
    keywords=["TL-MR6400", "influxdb", "LTE"],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    include_package_data=True,
    install_requires=REQUIRES,
    setup_requires=[
        'pytest-runner', 'wheel', 'twine'
    ],
    packages=find_packages(),
    long_description="""\
    Tool to read stats from TL-MR6400 LTE router and push these to influxdb
    """
)
