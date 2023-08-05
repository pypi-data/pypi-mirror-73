import os

import setuptools
from setuptools.command.develop import develop
from setuptools.command.install import install

with open("README.md", "r") as fh:
    long_description = fh.read()

class PostDevelopCommand(develop):
    """Post-installation for development mode."""
    def run(self):
        develop.run(self)
        os.system('./bin/install_requirements.txt')
        os.system('./bin/')
        

class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        install.run(self)
        os.system('./bin/install_requirements.txt')
        os.system('./bin/equities/test.py')
        

setuptools.setup(
    name="equities", # Replace with your own username
    version="1.2.5",
    author="Luigi Charles",
    author_email="ljwcharles@gmail.com",
    description="equities aims to democratize access to publically avaliable financial data. sec data scrapper/parser/cleaner ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ljc-codes/art-engine.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    scripts=["./bin/install_requirements.sh",
             "./equities/test.py"],
    keywords="sec stock stockmarket equities equity scrapper parser pandas",
    python_requires='>=3.6',
)