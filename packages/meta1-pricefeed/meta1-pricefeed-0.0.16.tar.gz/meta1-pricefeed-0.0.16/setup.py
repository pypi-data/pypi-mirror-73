#!/usr/bin/env python

from setuptools import setup, find_packages
import sys

__VERSION__ = '0.0.16'

assert sys.version_info[0] == 3, "Meta1-PriceFeed requires Python > 3"

setup(
    name='meta1-pricefeed',
    version=__VERSION__,
    description='Command line tool to assist with price feed generation',
    long_description='t.me/Avowe',
    download_url='https://github.com/xeroc/meta1-pricefeed/tarball/' + __VERSION__,
    author='Fabian Schuh',
    author_email='Fabian@chainsquad.com',
    maintainer='Fabian Schuh',
    maintainer_email='Fabian@chainsquad.com',
    url='http://www.github.com/xeroc/meta1-pricefeed',
    keywords=['meta1', 'price', 'feed', 'cli'],
    packages=find_packages(),
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
    ],
    entry_points={
        'console_scripts': [
            'meta1-pricefeed = meta1_pricefeed.cli:main'
        ],
    },
    install_requires=[
        "requests==2.22.0", # Required by graphenlib
        "meta1",
        "muptick",
        "prettytable",
        "click",
        "colorama",
        "tqdm",
        "pyyaml",
        "quandl"
    ],
    extras_require = {
        'history_db_postgresql':  ["SQLAlchemy", "py-postgresql"]
    },
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    include_package_data=True,
)
