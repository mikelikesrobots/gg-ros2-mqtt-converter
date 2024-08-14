#!/bin/bash
set -e

docker build -t "$ECR_REPO/aws-iot-robot-connectivity-samples-ros2:latest" .
