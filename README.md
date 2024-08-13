# ROS2 MQTT Converter Greengrass Component

This repository defines how to build a Greengrass component that will subscribe to ROS2 topics, convert the messages to JSON format, and send them to AWS IoT Core automatically. All that needs to be changed is the configuration of the component in the deployment, as long as the message types of the topic are available on the Greengrass system.

This project is based on another project for building multiple Docker images into one or more Greengrass components, which can be found [here](https://github.com/mikelikesrobots/greengrass-docker-compose). This includes extra permissions that need to be granted to Greengrass in AWS to be able to pull from ECR and S3, which are required for correct functioning of the components.

Make sure that [Docker](https://get.docker.com/), the [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html), and the [Greengrass Development Kit](https://docs.aws.amazon.com/greengrass/v2/developerguide/install-greengrass-development-kit-cli.html) are installed.

## Checking out the code

To check out the code, execute the following:

```bash
git clone https://github.com/mikelikesrobots/gg-ros2-mqtt-converter
cd gg-ros2-mqtt-converter
git submodule update --init --recursive
```

## Building and Publishing

To build and publish the Greengrass component and related Docker images, first create the ECR repositories for the Docker images:

1. `aws-iot-robot-connectivity-samples-ros2`
1. `ros2-mqtt-converter`

Once complete, edit the `.env` file with the base URI of either of the ECR repositories. For example, if your ECR URI is `123456789012.dkr.ecr.us-west-2.amazonaws.com/aws-iot-robot-connectivity-samples-ros2`, then `.env` should contain:

```bash
ECR_REPO=123456789012.dkr.ecr.us-west-2.amazonaws.com
```

Once complete, execute the following two scripts:

```bash
./build_all.sh
./publish_all.sh
```

With the completion of these scripts, your Docker images have been built and pushed, and your Greengrass component is ready for deployment.

## Testing on a Greengrass system

This repository includes a helper script for setting up the current system as a Greengrass core device and will deploy the new component to it. To set it up, make sure the AWS CLI is installed and has sufficient permissions for Greengrass, then execute:

```bash
./scripts/greengrass_deployment_config.json
```

Once complete, wait a short time for the system to start up and accept the deployment, then access the MQTT test client in the cloud. By subscribing to `#` as a topic filter, you should be able to see simulated data from 3 robots being sent in to the cloud. None of these devices need any knowledge of IoT software or certificates - they publish data on ROS2 topics as normal, and the Greengrass component is responsible for subscribing and converting the messages!

## Next Steps

This repository includes the mock data generator only as an example. For real use, this Docker image can be stripped out and removed from the Docker Compose file. In addition, this component is only capable of converting message formats included in the base ROS2 installation; to include extra message formats, the packages containing those formats also need to be included in the Docker image. This can be done by modifying the Dockerfile to include the message packages in the workspace, such that they are built and sourced as part of the ROS2 workspace.
