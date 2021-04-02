#!/bin/bash
docker build . -t rest_api:latest
docker run --name rest_api -p 8000:8000 -d --rm rest_api
