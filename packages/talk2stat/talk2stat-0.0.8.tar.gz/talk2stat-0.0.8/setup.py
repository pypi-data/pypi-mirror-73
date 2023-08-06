import os
import setuptools

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.txt')) as f:
    long_description = f.read()

setuptools.setup(
    name="talk2stat",
    version="0.0.8",
    author="Haim Bar",
    author_email="haim.bar@uconn.edu",
    description="Open a bidirectional pipe to R, julia, matlab, or python (etc.) and communicate with it via a socket.",
    url = "http://packages.python.org/an_example_pypi_project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['talk2stat'],
    install_requires=["pexpect"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
