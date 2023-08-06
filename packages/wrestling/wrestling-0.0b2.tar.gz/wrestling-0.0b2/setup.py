# setup

from setuptools import setup, find_packages

# read the contents of your README file
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

requirements = ["aenum", "attrs", "wheel"]

setup(
    name="wrestling",
    version="0.0.b2",
    author="Nicholas Anthony",
    author_email="nanthony007@gmail.com",
    description="A package for wrestling statistics and visualizations.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nanthony007/wrestling/",
    packages=find_packages(),
    install_requires=requirements,
    # classifiers=[
    #     "Programming Language :: Python :: 3.8",
    #     "License :: OSI Approved :: MIT License",
    #     "Development Status :: 4-Beta",
    # ],
)
