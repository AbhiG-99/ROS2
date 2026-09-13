#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exercise 2 — Static broadcaster for a two-sensor robot.

Publishes TWO static transforms from a SINGLE node:

    base_link -> laser        (x=0.20, y=0.00, z=0.15, yaw=0 deg)
    base_link -> camera_link  (x=0.10, y=0.00, z=0.40, yaw=90 deg)

Verify with:
    ros2 run tf2_ros tf2_echo base_link camera_link
    ros2 run tf2_ros tf2_echo laser camera_link
"""
import math

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TransformStamped
from tf2_ros import StaticTransformBroadcaster


class SensorMounts(Node):
    def __init__(self):
        super().__init__('sensor_mounts')
        self.br = StaticTransformBroadcaster(self)
        self.publish_mounts()
        self.get_logger().info(
            "Published static transforms: "
            "base_link->laser (0.20, 0, 0.15, yaw 0 deg), "
            "base_link->camera_link (0.10, 0, 0.40, yaw 90 deg)")

    def make_static(self, parent, child, x, y, z, yaw):
        t = TransformStamped()
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = parent
        t.child_frame_id = child
        t.transform.translation.x = x
        t.transform.translation.y = y
        t.transform.translation.z = z
        # yaw-only rotation about Z
        t.transform.rotation.z = math.sin(yaw / 2.0)
        t.transform.rotation.w = math.cos(yaw / 2.0)
        return t

    def publish_mounts(self):
        laser = self.make_static('base_link', 'laser',
                                 0.20, 0.00, 0.15, 0.0)                 # yaw 0 deg
        camera = self.make_static('base_link', 'camera_link',
                                  0.10, 0.00, 0.40, math.pi / 2.0)      # yaw 90 deg
        self.br.sendTransform([laser, camera])


def main(args=None):
    rclpy.init(args=args)
    node = SensorMounts()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()