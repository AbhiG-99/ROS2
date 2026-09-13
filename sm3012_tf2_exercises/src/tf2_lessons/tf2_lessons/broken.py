#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exercise 8 — THE FIXED BROKEN BROADCASTER.

All four bugs from the original are fixed here:

    BUG 1 (leading slash)    : header.frame_id = 'odom'          (no '/')
    BUG 2 (stale timestamp)  : stamp refreshed inside tick()     (was set once
                               in __init__, then reused forever)
    BUG 3 (zero quaternion)  : rotation built from yaw           (w=0.0 with
                               x=y=z=0 is NOT normalized -> TF drops it)
    BUG 4 (static rotation)  : rotation updated every tick       (robot now
                               faces its direction of travel)

Run alongside odometer.py:
    ros2 run tf2_lessons broken
    ros2 run tf2_lessons odometer
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

        # FIX 1: no leading slash
        self.msg.header.frame_id = 'odom'
        self.msg.child_frame_id = 'base_link'
        self.msg.transform.translation.z = 0.0

        self.create_timer(0.05, self.tick)

    def tick(self):
        el = (self.get_clock().now() - self.t0).nanoseconds * 1e-9

        # FIX 2: refresh the stamp every tick
        self.msg.header.stamp = self.get_clock().now().to_msg()

        x = 2.0 * math.cos(0.4 * el)
        y = 2.0 * math.sin(0.4 * el)
        # robot drives a circle -> face the velocity (yaw = angle + pi/2)
        yaw = math.atan2(math.cos(0.4 * el), -math.sin(0.4 * el))

        self.msg.transform.translation.x = x
        self.msg.transform.translation.y = y

        # FIX 3 + 4: normalized, updated quaternion (yaw about Z)
        self.msg.transform.rotation.x = 0.0
        self.msg.transform.rotation.y = 0.0
        self.msg.transform.rotation.z = math.sin(yaw / 2.0)
        self.msg.transform.rotation.w = math.cos(yaw / 2.0)

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