#!/bin/bash

COMMIT_HASH=$(git rev-parse --short=7 HEAD)
IMAGE_NAME="rinhac"
IMAGE_TAG="$COMMIT_HASH"
docker build -t "${IMAGE_NAME}:${IMAGE_TAG}" .
