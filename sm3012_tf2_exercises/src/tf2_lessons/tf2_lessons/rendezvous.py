#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exercise 9 — Rendezvous node (runs at 2 Hz).

Reports, for Robot A relative to Robot B:
    1. Range   — straight-line distance from robot_a to robot_b
    2. Bearing — angle of robot_b in robot_a's frame (deg)
    3. In-FOV  — is robot_b inside robot_a's 60 deg FORWARD field of view
                 (i.e. bearing within +-30 deg of robot_a's +x axis)?
    4. Past pose — where robot_b was 1.5 s ago, expressed in
                   robot_a's CURRENT frame.

Frames used (published by robot_a.py / robot_b.py):
    world -> robot_a -> robot_a/front_sensor
    world -> robot_b -> robot_b/front_sensor

Run:
    ros2 run tf2_lessons robot_a
    ros2 run tf2_lessons robot_b
    ros2 run tf2_lessons rendezvous
"""
import math

import rclpy
from rclpy.node import Node
from rclpy.duration import Duration
from tf2_ros import Buffer, TransformListener, TransformException

FOV_HALF = math.radians(30.0)   # 60 deg field, half on each side of +x
LOOKBACK = Duration(seconds=1.5)


class Rendezvous(Node):
    def __init__(self):
        super().__init__('rendezvous')
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        self.create_timer(0.5, self.report)     # 2 Hz

    @staticmethod
    def to_pose2d(tf):
        """Extract (x, y, yaw) from a TransformStamped (yaw-only motion)."""
        qz = tf.transform.rotation.z
        qw = tf.transform.rotation.w
        yaw = 2.0 * math.atan2(qz, qw)
        return (tf.transform.translation.x,
                tf.transform.translation.y,
                yaw)

    def report(self):
        now = self.get_clock().now()
        try:
            # ---- 1) + 2) range & bearing, robot_b in robot_a's frame ----
            t_ab = self.tf_buffer.lookup_transform('robot_a', 'robot_b',
                                                   rclpy.time.Time())
            x, y, _ = self.to_pose2d(t_ab)
            rng = math.hypot(x, y)
            bearing = math.atan2(y, x)          # angle from robot_a +x axis

            # ---- 3) 60 deg forward FOV check ----
            in_fov = abs(bearing) <= FOV_HALF

            # ---- 4) robot_b 1.5 s ago in robot_a's CURRENT frame ----
            #  T(A-only) = inv(world->robot_a at now)
            #            * (world->robot_b at now - 1.5 s)
            t_w_a_now = self.tf_buffer.lookup_transform('world', 'robot_a', now)
            t_w_b_past = self.tf_buffer.lookup_transform(
                'world', 'robot_b', now - LOOKBACK)
            ax, ay, ayaw = self.to_pose2d(t_w_a_now)
            bx, by, byaw = self.to_pose2d(t_w_b_past)

            dx, dy = bx - ax, by - ay
            c, s = math.cos(-ayaw), math.sin(-ayaw)
            b_local_x = c * dx - s * dy         # rotate into robot_a's frame
            b_local_y = s * dx + c * dy
            b_local_yaw = byaw - ayaw
        except TransformException as e:
            self.get_logger().warn(f'Could not get transform: {e}')
            return

        self.get_logger().info(
            f'range={rng:.3f} m | bearing={math.degrees(bearing):7.1f} deg | '
            f'B in 60deg FOV: {"YES" if in_fov else "no"} | '
            f'B was 1.5 s ago @ A-now: '
            f'({b_local_x:.3f}, {b_local_y:.3f}) yaw={math.degrees(b_local_yaw):.1f} deg')


def main(args=None):
    rclpy.init(args=args)
    node = Rendezvous()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()