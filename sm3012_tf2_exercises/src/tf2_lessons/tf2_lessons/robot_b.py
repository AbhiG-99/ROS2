#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exercise 9 — Robot B (rendezvous mini-project).

Publishes `world -> robot_b` at 50 Hz:
    circle radius   = 1.5 m
    angular speed   = 0.7 rad/s
    OPPOSITE direction (clockwise)  =>  OMEGA = -0.7

Also publishes the static sensor mount:
    robot_b -> robot_b/front_sensor , 0.25 m forward (along +x)
"""
import math

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TransformStamped
from tf2_ros import TransformBroadcaster, StaticTransformBroadcaster

RADIUS = 1.5
OMEGA = -0.7         # negative => clockwise (opposite of Robot A)
HZ = 50.0


class RobotB(Node):
    def __init__(self):
        super().__init__('robot_b')
        self.br = TransformBroadcaster(self)
        self.static_br = StaticTransformBroadcaster(self)
        self.t0 = self.get_clock().now()
        self.publish_sensor_mount()
        self.create_timer(1.0 / HZ, self.tick)

    def publish_sensor_mount(self):
        t = TransformStamped()
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = 'robot_b'
        t.child_frame_id = 'robot_b/front_sensor'
        t.transform.translation.x = 0.25      # 0.25 m forward
        t.transform.translation.y = 0.0
        t.transform.translation.z = 0.0
        t.transform.rotation.w = 1.0
        self.static_br.sendTransform(t)

    def tick(self):
        t = (self.get_clock().now() - self.t0).nanoseconds * 1e-9
        theta = OMEGA * t

        x = RADIUS * math.cos(theta)
        y = RADIUS * math.sin(theta)
        # velocity -> heading
        yaw = math.atan2(RADIUS * OMEGA * math.cos(theta),
                         -RADIUS * OMEGA * math.sin(theta))

        msg = TransformStamped()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'world'
        msg.child_frame_id = 'robot_b'
        msg.transform.translation.x = x
        msg.transform.translation.y = y
        msg.transform.translation.z = 0.0
        msg.transform.rotation.z = math.sin(yaw / 2.0)
        msg.transform.rotation.w = math.cos(yaw / 2.0)
        self.br.sendTransform(msg)


def main(args=None):
    rclpy.init(args=args)
    node = RobotB()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()