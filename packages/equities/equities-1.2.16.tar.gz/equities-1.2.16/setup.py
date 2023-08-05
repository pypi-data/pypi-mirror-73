import os

import setuptools
import setuptools.command.build_py
import distutils.cmd
import distutils.log
import subprocess

with open('requirements.txt') as f:
    required = f.read().splitlines()

class BuildPyCommand(setuptools.command.build_py.build_py):
  """Custom build command."""

  def run(self):
    self.run_command('requirements')
    setuptools.command.build_py.build_py.run(self)

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="equities", # Replace with your own username
    version="1.2.16",
    author="Luigi Charles",
    author_email="ljwcharles@gmail.com",
    description="equities aims to democratize access to publically avaliable financial data. sec data scrapper/parser/cleaner ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ljc-codes/art-engine.git",
    packages=setuptools.find_packages(include=["*.csv"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=required,
    keywords="sec stock stockmarket equities equity scrapper parser pandas",
    python_requires='>=3.6',
)