#!/bin/bash

set -e

cd "$(dirname "$0")/project-be-books"

docker-compose up
