#!/bin/bash
set -e

aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin $ECR_REPO
docker push $ECR_REPO/aws-iot-robot-connectivity-samples-ros2:latest
