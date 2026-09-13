#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exercise 3 — A robot that moves (dynamic broadcaster).

Publishes odom -> base_link at 50 Hz tracing a figure-eight (lemniscate):

    x(t) = A * sin(w*t)
    y(t) = A * sin(w*t) * cos(w*t)

    A = 2.0
    w = 0.5 rad/s

Additional requirement: the robot must FACE ITS DIRECTION OF TRAVEL,
so yaw is computed from the velocity vector (atan2 of xdot, ydot).

Note: with these exact equations the lemniscate crosses the origin along
the 45 deg diagonal, so at t=0 the heading is 45 deg (see docs/predictions.md
for the Exercise 6 discussion).

Visualize in RViz2 with Fixed Frame = odom; run sensor_mounts.py
alongside to see the laser/camera frames ride along.
"""
import math

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TransformStamped
from tf2_ros import TransformBroadcaster

A = 2.0          # amplitude (m)
OMEGA = 0.5      # angular frequency (rad/s)
HZ = 50.0        # publish rate


class FigureEight(Node):
    def __init__(self):
        super().__init__('figure_eight')
        self.br = TransformBroadcaster(self)
        self.t0 = self.get_clock().now()
        self.create_timer(1.0 / HZ, self.tick)

    def tick(self):
        t = (self.get_clock().now() - self.t0).nanoseconds * 1e-9

        # Position on the lemniscate
        x = A * math.sin(OMEGA * t)
        y = A * math.sin(OMEGA * t) * math.cos(OMEGA * t)

        # Velocity -> heading of the robot
        xdot = A * OMEGA * math.cos(OMEGA * t)
        ydot = A * OMEGA * (math.cos(OMEGA * t) ** 2
                            - math.sin(OMEGA * t) ** 2)
        yaw = math.atan2(ydot, xdot)

        msg = TransformStamped()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'odom'
        msg.child_frame_id = 'base_link'
        msg.transform.translation.x = x
        msg.transform.translation.y = y
        msg.transform.translation.z = 0.0
        msg.transform.rotation.z = math.sin(yaw / 2.0)   # yaw-only rotation
        msg.transform.rotation.w = math.cos(yaw / 2.0)
        self.br.sendTransform(msg)


def main(args=None):
    rclpy.init(args=args)
    node = FigureEight()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()