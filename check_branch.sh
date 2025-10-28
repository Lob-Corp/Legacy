#!/bin/bash

if [ "$#" -ne 2 ]; then
    echo "Error: Expected 2 arguments, got $#."
    echo "Usage: $0 <base_branch> <head_branch>"
    exit 1
fi

BASE_BRANCH="$1"
HEAD_BRANCH="$2"

fail() {
    echo "Branch merging rule violation: $1"
    exit 1
}

if [ "$BASE_BRANCH" = "main" ]; then
    if [[ ! "$HEAD_BRANCH" =~ ^milestone\/.+$ ]] && \
    [[ ! "$HEAD_BRANCH" =~ ^hotfix\/.+$ ]] && \
    [[ ! "$HEAD_BRANCH" =~ ^docs\/global\/.+$ ]]; then
        fail "Only 'milestone/*', 'hotfix/*', or 'docs/global/*' branches can be merged into 'main'."
    fi
fi

if [[ "$BASE_BRANCH" =~ ^milestone\/(.+)$ ]]; then
    MILESTONE_NAME="${BASH_REMATCH[1]}"
    if [[ ! "$HEAD_BRANCH" =~ .*/${MILESTONE_NAME}/.* ]]; then
        fail "Only branches matching '*/${MILESTONE_NAME}/*' can be merged into 'milestone/${MILESTONE_NAME}'."
    fi
fi
