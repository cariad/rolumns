#!/bin/env bash

set -euo pipefail

cd docs
rm -rf build
make doctest
make html
