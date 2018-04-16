#!/usr/bin/env bash

psql --host=wp7th.cuhzbappzv2q.ap-northeast-2.rds.amazonaws.com --user=archo --port=5432 postgres <<EOF
DROP DATABASE overeats;
CREATE DATABASE overeats;
\c overeats;
CREATE EXTENSION postgis;
EOF