#!/usr/bin/env bash

git add -f .secrets && eb deploy --staged --profile=overeats; git reset HEAD .secrets