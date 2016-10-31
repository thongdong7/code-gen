#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='code-gen',
    version='0.1.0.dev',
    description='Code Gen',
    author='Thong Dong',
    author_email='thongdong7@gmail.com',
    url='https://github.com/thongdong7/code-gen',
    packages=find_packages(exclude=["build", "dist", "tests*"]),
    install_requires=[
        'pyyaml',
        'click==6.6',
        'jinja2==2.8',
        'pyfunctional==0.8.0',
    ],
    # extras_require={
    #     'cli': [
    #         'click==6.6',
    #         'pyyaml==3.11'
    #     ],
    # },
    entry_points={
        'console_scripts': [
            'code-gen=code_gen.scripts:cli',
        ],
    },
    include_package_data=True,
)
