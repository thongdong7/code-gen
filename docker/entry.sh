#!/usr/bin/env bash
set -ex

TARGET=dist/code-gen-$(uname -s)-$(uname -m)

./venv/bin/pip install -e .
./venv/bin/pyinstaller code-gen.spec
mv dist/code-gen $TARGET
