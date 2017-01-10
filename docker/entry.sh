#!/usr/bin/env bash
set -ex

TARGET=dist/zander-$(uname -s)-$(uname -m)

./venv/bin/pip install -e .
./venv/bin/pyinstaller zander.spec
mv dist/code-gen $TARGET
