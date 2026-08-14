#!/usr/bin/env python3

import time

import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32MultiArray
import RPi.GPIO as GPIO


STEP_PIN = 17
DIR_PIN = 18


class StepperNode(Node):
    def __init__(self):
        super().__init__('motor_driver')

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(STEP_PIN, GPIO.OUT)
        GPIO.setup(DIR_PIN, GPIO.OUT)

        GPIO.output(DIR_PIN, GPIO.HIGH)

        self.subscription = self.create_subscription(Int32MultiArray, 'stepper_cmd', self.stepper_cmd_callback, 10)
        self.get_logger().info(
            '(steps, stepDelay).'
        )

    def stepper_cmd_callback(self, msg):
        steps = msg.data[0]
        delay = msg.data[1]/1000.0

        direction = GPIO.HIGH if steps >= 0 else GPIO.LOW
        GPIO.output(DIR_PIN, direction)
        steps = abs(steps)

        self.get_logger().info(
            f'Rotating {steps} steps {"CW" if direction == 1 else "CCW"}'
        )

        for i in range(steps):
            GPIO.output(STEP_PIN, GPIO.HIGH)
            time.sleep(delay)
            GPIO.output(STEP_PIN, GPIO.LOW)
            time.sleep(delay)

    def destroy_node(self):
        GPIO.cleanup()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    stepper_node = StepperNode()
    rclpy.spin(stepper_node)
    stepper_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()