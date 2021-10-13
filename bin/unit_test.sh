#!/usr/bin/env sh

set -e

echo "Linting Started.."
flake8  && isort --check --diff .
echo "Linting done!"

echo "Testing User_API has Started!!"

python -W always::DeprecationWarning -m pytest -s


echo "Testing phase has ended."
