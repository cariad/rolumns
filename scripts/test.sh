#!/bin/env bash

set -euo pipefail

pytest -vv

cd docs
make doctest
