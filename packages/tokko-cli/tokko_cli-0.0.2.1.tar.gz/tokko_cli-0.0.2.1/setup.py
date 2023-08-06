#!/usr/bin/python3

import os
from setuptools import find_packages, setup

readme_file = os.path.join(os.path.dirname(__file__), 'README.md')

with open(readme_file) as readme:
    README = f"{readme.read()}"
README = README.replace(README.split('# Install')[0], '')

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name="tokko_cli",
    version="0.0.2.1",
    packages=find_packages(),
    include_package_data=True,
    license="BSD License",
    description="Radioactive Unicorns",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/TokkoLabs/services-tokkobroker/tools/tokko-cli",
    author="Jose Salgado",
    author_email="jsalgado@navent.com",
    install_requires=[
        "tokko-rpc==0.0.2",
        "click==7.1.2",
        "arrow==0.15.6",
        "pyaml==20.4.0",
        "jinja2==2.11.2",
        "distro==1.5.0",
        "GitPython==3.1.7",
        "requests==2.24.0",
        "coloredlogs==14.0 ",
    ],
    entry_points='''
        [console_scripts]
        tokky=tokko_cli.cli:main
    ''',
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 3.0",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
)

