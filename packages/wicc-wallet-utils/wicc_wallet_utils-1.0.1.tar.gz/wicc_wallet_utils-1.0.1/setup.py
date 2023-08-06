#!/usr/bin/python
# -*- coding: utf-8 -*-
import setuptools
import io

with io.open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    # name="waykichain",
    name="wicc_wallet_utils",
    version="1.0.1",
    author="WaykiChain CoreDev",
    author_email="coredev@waykichainhk.com",
    description="WaykiChain Wallet Utils",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/WaykiChain/wicc-wallet-utils-python",
    packages=setuptools.find_packages(),
    install_requires=[
        'cryptos==1.36',
        'requests',
        'pbkdf2'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
