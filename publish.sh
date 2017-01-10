#!/usr/bin/env bash

set -e

rm -rf build || true
rm -rf dist || true

echo Upload packages...
python setup.py bdist_wheel --universal upload -r pypi
