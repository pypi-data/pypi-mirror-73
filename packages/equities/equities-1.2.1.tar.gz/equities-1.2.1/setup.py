import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="equities", # Replace with your own username
    version="1.2.1",
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
    keywords="sec stock stockmarket equities equity scrapper parser pandas",
    python_requires='>=3.6',
)