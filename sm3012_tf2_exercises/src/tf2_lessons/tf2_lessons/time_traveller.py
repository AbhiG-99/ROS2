#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exercise 7 — Time travel.

Once per second prints:
    1. Robot's position NOW
    2. Robot's position 2 SECONDS AGO
    3. Distance between the two
    4. Attempts a lookup 30 SECONDS in the past and reports the
       exception cleanly (deliberately outside the TF buffer cache).

The tf2 buffer is time-indexed; its default cache is only 5 seconds,
so a 30-second-old query must fail with an Extrapolation/Lookup error.
"""
import math

import rclpy
from rclpy.node import Node
from rclpy.duration import Duration
from tf2_ros import Buffer, TransformListener, TransformException


class TimeTraveller(Node):
    def __init__(self):
        super().__init__('time_traveller')
        self.tf_buffer = Buffer()          # default cache duration = 5 s
        self.tf_listener = TransformListener(self.tf_buffer, self)
        self.create_timer(1.0, self.report)

    def xy_at(self, stamp):
        tf = self.tf_buffer.lookup_transform('odom', 'base_link', stamp)
        return (tf.transform.translation.x, tf.transform.translation.y)

    def report(self):
        now = self.get_clock().now()

        # 1) position now (latest transform)
        try:
            x_now, y_now = self.xy_at(rclpy.time.Time())
        except TransformException as e:
            self.get_logger().warn(f'No transform yet (now): {e}')
            return

        # 2) position 2 seconds ago
        try:
            x_past, y_past = self.xy_at(now - Duration(seconds=2.0))
        except TransformException as e:
            self.get_logger().warn(f'No history 2 s ago: {e}')
            return

        # 3) distance between the two
        dist = math.hypot(x_now - x_past, y_now - y_past)

        self.get_logger().info(
            f'now=({x_now:.3f}, {y_now:.3f})  2s ago=({x_past:.3f}, {y_past:.3f})  '
            f'moved={dist:.3f} m')

        # 4) 30 seconds in the past -> outside the 5 s cache -> exception
        try:
            x_old, y_old = self.xy_at(now - Duration(seconds=30.0))
            self.get_logger().info(f'30s ago: ({x_old:.3f}, {y_old:.3f})')
        except TransformException as e:
            self.get_logger().info(
                f'30 s lookup failed as expected -> '
                f'{type(e).__name__}: {e}')


def main(args=None):
    rclpy.init(args=args)
    node = TimeTraveller()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()