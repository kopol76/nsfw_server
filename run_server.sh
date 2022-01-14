#!/usr/bin/env bash
docker run \
--rm \
-ti \
-p 28000:28000 \
-d \
nsfw_server:v1 \
python3 server.py 28000

#bash