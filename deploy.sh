#!/usr/bin/env bash

git add -f .secrets && eb deploy --staged --profile=eb; git reset HEAD .secrets