#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exercise 8 — THE ORIGINAL BROKEN BROADCASTER (do NOT run this one!).

This file is kept exactly as given in the assignment so you can demo the
errors. Run it next to odometer.py and observe the four failures:

    1. '/odom' leading slash        -> "Invalid frame ID '/odom'"
    2. stamp set once, never updated-> extrapolation into the past
    3. rotation.w = 0.0             -> "Invalid rotation quaternion"
    4. rotation never set in tick() -> robot never turns, yaw is garbage

The FIXED version is the companion file `broken.py`.
"""
import math
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TransformStamped
from tf2_ros import TransformBroadcaster


class Broken(Node):
    def __init__(self):
        super().__init__('broken')
        self.br = TransformBroadcaster(self)
        self.t0 = self.get_clock().now()
        self.msg = TransformStamped()

        self.msg.header.stamp = self.get_clock().now().to_msg()  # BUG 2: stale stamp
        self.msg.header.frame_id = '/odom'                       # BUG 1: leading slash
        self.msg.child_frame_id = 'base_link'

        self.msg.transform.translation.z = 0
        self.msg.transform.rotation.w = 0.0                      # BUG 3+4: zero quaternion

        self.create_timer(0.05, self.tick)

    def tick(self):
        el = (self.get_clock().now() - self.t0).nanoseconds * 1e-9
        self.msg.transform.translation.x = 2.0 * math.cos(0.4 * el)
        self.msg.transform.translation.y = 2.0 * math.sin(0.4 * el)
        self.br.sendTransform(self.msg)


def main(args=None):
    rclpy.init(args=args)
    node = Broken()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()