#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exercise 4 — Listener: how far has the robot travelled?

Once per second reports:
    1. Robot's current position in `odom`
    2. Straight-line distance from the origin
    3. Yaw in degrees

IMPORTANT: must survive being started BEFORE the broadcaster.
If the transform is not available yet -> warn, don't crash, try again.
"""
import math

import rclpy
from rclpy.node import Node
from tf2_ros import Buffer, TransformListener, TransformException


class Odometer(Node):
    def __init__(self):
        super().__init__('odometer')
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        self.create_timer(1.0, self.report)

    def report(self):
        # Time() with no args = "latest available transform"
        try:
            tf = self.tf_buffer.lookup_transform('odom', 'base_link',
                                                 rclpy.time.Time())
        except TransformException as e:
            # Started before the broadcaster -> warn, do NOT crash.
            self.get_logger().warn(
                f'Transform odom->base_link not available yet: {e}')
            return

        x = tf.transform.translation.x
        y = tf.transform.translation.y
        dist = math.hypot(x, y)

        # Yaw from the quaternion (generic formula, works for any orientation)
        qx = tf.transform.rotation.x
        qy = tf.transform.rotation.y
        qz = tf.transform.rotation.z
        qw = tf.transform.rotation.w
        yaw = math.atan2(2.0 * (qw * qz + qx * qy),
                         1.0 - 2.0 * (qy * qy + qz * qz))

        self.get_logger().info(
            f'pos=({x:.3f}, {y:.3f})  distance={dist:.3f} m  '
            f'yaw={math.degrees(yaw):.1f} deg')


def main(args=None):
    rclpy.init(args=args)
    node = Odometer()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()