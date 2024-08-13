#!/usr/bin/env python3

from awsiot.greengrasscoreipc.clientv2 import GreengrassCoreIPCClientV2
from awsiot.greengrasscoreipc.model import BinaryMessage, PublishMessage
import json
import os
import rclpy
from rclpy.node import Node
from rosidl_runtime_py import message_to_ordereddict


class Ros2MqttConverter(Node):
    def __init__(self):
        super().__init__("ros2_mqtt_converter")

        self._ipc_client = GreengrassCoreIPCClientV2()

        self._timer = self.create_timer(5, self._on_timer)
        # Config will be a JSON escaped string of topics
        escaped_config = os.environ.get("ROS2_TOPICS", r"\"[\"]")
        inner_config = json.loads(escaped_config)
        self._config = json.loads(inner_config)
        self.get_logger().info("Got config: {}".format(self._config))

        self._dynamic_subscriptions = {}
        self._update_subscriptions()

    def _subscribe_to(self, topic_name, topic_type):
        logger = self.get_logger()
        logger.info("Creating subscription to topic {}".format(topic_name))
        pkg = ".".join(topic_type.split("/")[:-1])
        _cls = topic_type.split("/")[-1]
        logger.info("from {} import {}".format(pkg, _cls))
        msg_type = getattr(__import__(pkg, globals(), locals(), [_cls], 0), _cls)

        sub = self.create_subscription(
            msg_type,
            topic_name,
            lambda msg: self._callback(topic_name, msg),
            10
        )
        # self._subscriptions is in use by the base class
        self._dynamic_subscriptions[topic_name] = sub

    def _callback(self, topic_name, msg):
        mqtt_topic = "robots/" + topic_name
        mqtt_topic = mqtt_topic.replace("//", "/")

        ordered_dict = message_to_ordereddict(msg)
        mqtt_msg = json.dumps(ordered_dict)

        self.get_logger().info("Publishing on topic {} with message {}".format(mqtt_topic, mqtt_msg))

        binary_message = BinaryMessage(message=bytes(mqtt_msg, "utf-8"))
        publish_message = PublishMessage(binary_message=binary_message)
        self._ipc_client.publish_to_topic(topic=mqtt_topic, publish_message=publish_message)

    def _update_subscriptions(self):
        topic_tuples = self.get_topic_names_and_types()
        available_topics = dict((key, val[0]) for key, val in topic_tuples)
        for topic in self._config:
            # topic already exists in both? Continue
            if topic in available_topics and topic in self._dynamic_subscriptions:
                self.get_logger().info("Subbed to {} already".format(topic))
                continue
            # if topic is subscribed but has no topic name, delete
            elif topic not in available_topics and topic in self._dynamic_subscriptions:
                self.get_logger().info("Destroying sub for {}".format(topic))
                self.destroy_subscription(self._dynamic_subscriptions.pop(topic))
            # if topic is not subscribed but should be, subscribe to it
            elif topic in available_topics and topic not in self._dynamic_subscriptions:
                self._subscribe_to(topic, available_topics[topic])

    def _on_timer(self):
        self._update_subscriptions()


def main(args=None):
    rclpy.init(args=args)
    converter = Ros2MqttConverter()
    rclpy.spin(converter)

    converter.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
