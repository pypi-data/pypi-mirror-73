import os
from setuptools import setup, find_packages

setup(
    name = "iq-djangocms-utils",
    version = "0.1",
    author = "Lutz Mende",
    author_email = "lutz.mende@inquant.de",
    description = "DjangoCMS-Utils - a Product by InQuant",
    long_description=open("README.txt").read() + "\n" +
                     open("HISTORY.txt").read(),
    license = "GPL",
    packages = find_packages(),
    include_package_data = True,
    keywords = "django utils helpers",
    url = "http://www.inquant.de",
)


