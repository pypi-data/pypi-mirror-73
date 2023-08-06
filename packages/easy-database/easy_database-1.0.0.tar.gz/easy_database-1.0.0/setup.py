"""
This is the file used for creating the package
"""

import os.path
from setuptools import setup

# The directory containing this file
HERE = os.path.abspath(os.path.dirname(__file__))

# The text of the README file
with open("README.md") as fid:
    README = fid.read()

# This call to setup() does all the work
setup(
    name="easy_database",
    version="1.0.0",
    description="abstraction for ETL Database interaction",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/bclipp/easy_database",
    author="Brian Lipp",
    author_email="bclipp770@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    packages=["database"],
    include_package_data=False,
    install_requires=[
        "pandas", "psycopg2"
    ],
    entry_points={"console_scripts": ["easy_database=database.__main__:main"]},
)
