# -*- coding:utf-8 -*-


import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="havedocker",
    version="0.1.3.5",
    author="haitanghuadeng",
    author_email="491609917@qq.com",
    description="New havedocker, already has the basic docker instruction",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/haitanghuadeng",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
