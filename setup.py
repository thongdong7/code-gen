#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='zander',
    version='0.0.12',
    description='Code Generator',
    author='Thong Dong',
    author_email='thongdong7@gmail.com',
    url='https://github.com/thongdong7/code-gen',
    packages=find_packages(exclude=["build", "dist", "tests*"]),
    install_requires=[
        'pyyaml',
        'click==6.6',
        'jinja2==2.8',
        'pyfunctional',
        'tornado==4.4.2',
    ],
    # extras_require={
    #     'cli': [
    #         'click==6.6',
    #         'pyyaml==3.11'
    #     ],
    # },
    entry_points={
        'console_scripts': [
            'zander=zander.scripts:cli',
        ],
    },
    include_package_data=True,
)
