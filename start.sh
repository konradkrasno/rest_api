#!/bin/bash
sudo docker build . -t rest_api:latest
sudo docker run --name rest_api -p 8000:8000 -d --rm rest_api
