#!/bin/sh

COMMIT_HASH=$(git ls-remote https://github.com/FreedomDevs/svcLibs.git HEAD | awk '{print $1}')
echo "Файл prepare.sh отработал. Передан хэш: $COMMIT_HASH"
export DOCKER_BUILD_ARGS="--build-arg SVCLIBS_COMMIT=$COMMIT_HASH --build-arg VERSION=1.0"
