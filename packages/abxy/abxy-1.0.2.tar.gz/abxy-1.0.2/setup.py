import setuptools
import os

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="abxy", # Replace with your own username
    version="1.0.2",
    author="AbxyPlayz",
    author_email="InksterAbxyPY@protonmail.com",
    description="Abxy is a third party library for the package named inkster.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://pypi.org/project/abxy/",
    project_urls={
        "Discord": "https://discord.gg/HUFtMsz"
    },
    License='MIT',
    keywords='abxyplayz',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows :: Windows 10",
    ],
    python_requires='>=3.8',
)
