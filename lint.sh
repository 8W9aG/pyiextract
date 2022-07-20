#!/bin/bash

set -e

#mypy pyiextract --ignore-missing-import
#typecov 100 .typecov/report/linecount.txt
black pyiextract
autoflake --in-place --remove-unused-variables -r pyiextract
isort rc pyiextract
