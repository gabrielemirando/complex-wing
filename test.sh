#!/bin/bash

set -e

cd "$(dirname "$0")/project-be-books"

docker run --rm -it "$(docker build -q .)" poetry run ./manage.py test tests