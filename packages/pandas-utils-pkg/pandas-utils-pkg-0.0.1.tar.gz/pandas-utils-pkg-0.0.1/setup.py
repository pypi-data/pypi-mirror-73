import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pandas-utils-pkg",
    version="0.0.1",
    author="Thomas Dimnet",
    author_email="thomas.dimnet@gmail.com",
    description="A helper tool for pandans and mysql",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SensCritique/pandas-utils-pkg",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)