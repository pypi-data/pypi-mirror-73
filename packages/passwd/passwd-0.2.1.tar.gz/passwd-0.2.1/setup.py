import codecs
import os.path

import setuptools


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="passwd",
    version=get_version("passwd/__init__.py"),
    author="Benjamin Soyka",
    author_email="bensoyka@icloud.com",
    description="Assorted utilities for gracefully handling and generating passwords",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bsoyka/passwd",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.6',
    project_urls={
        "Documentation": "https://github.com/bsoyka/passwd/wiki",
        "Changelog": "https://github.com/bsoyka/passwd/blob/master/CHANGELOG.md"
    }
)
