#!/usr/bin/env sh

set -e

uvicorn main:app --host 0.0.0.0 --port 80 --reload
