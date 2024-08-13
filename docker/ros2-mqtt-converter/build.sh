#!/bin/bash
set -e

docker build -t $ECR_REPO/ros2-mqtt-converter:latest .
