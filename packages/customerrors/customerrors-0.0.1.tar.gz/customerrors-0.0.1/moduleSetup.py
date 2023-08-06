import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "customerrors",
    version = "0.0.1",
    author = "Splatboy Dev",
    author_email = "splatboy20081@gmail.com",
    description = ("A pypi test."),
    license = "GPL v3.0",
    keywords = "example documentation tutorial",
    url = "http://packages.python.org/customerrors",
    packages=['main', 'tests'],
    long_description=read('README.txt'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)
