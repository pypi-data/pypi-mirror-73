import os

import setuptools
import setuptools.command.build_py
import distutils.cmd
import distutils.log
import subprocess

class RequirementsCommand(distutils.cmd.Command):

  def initialize_options(self):
    """Set default values for options."""
    # Each user option must be listed here with their default value.
    self.pylint_rcfile = ''

  def finalize_options(self):
    """Post-process options."""
    if self.pylint_rcfile:
      assert os.path.exists(self.pylint_rcfile), (
          'Pylint config file %s does not exist.' % self.pylint_rcfile)

  def run(self):
    """Run command."""
    os.system('pip3 install -r requirements.txt --user')

class BuildPyCommand(setuptools.command.build_py.build_py):
  """Custom build command."""

  def run(self):
    self.run_command('requirements')
    setuptools.command.build_py.build_py.run(self)

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="equities", # Replace with your own username
    version="1.2.7",
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
    cmdclass={
        'build_py': BuildPyCommand,
        'requirements': RequirementsCommand
    },
    keywords="sec stock stockmarket equities equity scrapper parser pandas",
    python_requires='>=3.6',
)