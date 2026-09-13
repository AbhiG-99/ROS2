#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exercise 6 — Put an obstacle on the map.

The laser reports a hit at (1.5, 0.0, 0.0) in the **laser** frame,
once per second. We publish/print the SAME point expressed in `odom`.

The `laser` frame comes from Exercise 2 (sensor_mounts.py) and the
odom chain needs Exercise 3 (figure_eight.py) running.

Prediction at t=0 (see docs/predictions.md):
    robot at lemniscate origin facing +x
    laser mount offset (0.20, 0, 0.15) -> hit in odom ~ (1.70, 0.00, 0.15)
"""
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PointStamped
from tf2_ros import Buffer, TransformListener, TransformException


class ObstacleMapper(Node):
    def __init__(self):
        super().__init__('obstacle_mapper')
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        self.create_timer(1.0, self.map_hit)

    def map_hit(self):
        stamp = self.get_clock().now().to_msg()

        hit = PointStamped()
        hit.header.frame_id = 'laser'
        hit.header.stamp = stamp
        hit.point.x = 1.5
        hit.point.y = 0.0
        hit.point.z = 0.0

        try:
            # Ask the TF buffer to express the point in odom.
            # timeout: wait up to 1 s for the transform to become available.
            mapped = self.tf_buffer.transform(
                hit, 'odom', timeout=rclpy.duration.Duration(seconds=1.0))
        except TransformException as e:
            self.get_logger().warn(f'Could not transform hit to odom: {e}')
            return

        self.get_logger().info(
            f'Laser hit (1.5, 0, 0) in [laser]  ->  '
            f'({mapped.point.x:.3f}, {mapped.point.y:.3f}, '
            f'{mapped.point.z:.3f}) in [odom]')


def main(args=None):
    rclpy.init(args=args)
    node = ObstacleMapper()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()