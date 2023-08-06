# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='facebook_totem',
    version="1",
    packages=find_packages(),
    author="megadose",
    install_requires=["argparse","fake_useragent"],
    description="Totem allows you to retrieve information about ads of a facebook page , we can retrieve the number of people targeted, how much the ad cost and a lot of other information.",
    long_description="",
    include_package_data=True,
    url='http://github.com/megadose/facebook_totem',
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)
