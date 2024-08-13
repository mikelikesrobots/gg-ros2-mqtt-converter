FROM ros:humble-ros-base

WORKDIR /workspace
ADD ./aws-iot-robot-connectivity-samples-ros2/workspace/src /workspace/src
RUN bash -c "source /opt/ros/humble/setup.bash && colcon build"

ADD ./ros_entrypoint.sh /
