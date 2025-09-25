#!/bin/bash

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
