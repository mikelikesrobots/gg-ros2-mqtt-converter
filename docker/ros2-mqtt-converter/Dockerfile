FROM ros:humble-ros-base

RUN apt update && apt install -y python3-pip && apt clean
RUN pip install awsiotsdk

WORKDIR /workspace
ADD ./ros2-mqtt-converter /workspace/src
RUN bash -c "source /opt/ros/humble/setup.bash && colcon build"
ADD ./ros_entrypoint.sh /
