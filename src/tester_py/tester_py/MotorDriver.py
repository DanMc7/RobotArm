#!/usr/bin/env python3
"""
ROS2 (Humble, on Ubuntu 22.04) node that drives a NEMA 17 stepper motor
through an L298N H-bridge on a Raspberry Pi 3 B+.

Subscribes to:
    /stepper_cmd   (std_msgs/Int32)
        The sign of the value gives direction (positive = clockwise,
        negative = counter-clockwise). The magnitude is the number of
        steps to move. Example: publishing -100 rotates 100 steps
        counter-clockwise.

Wiring (BCM numbering) -- same as the standalone test script:
    L298N IN1 -> GPIO 17
    L298N IN2 -> GPIO 18
    L298N IN3 -> GPIO 27
    L298N IN4 -> GPIO 22
    Common ground between Pi, L298N, and motor power supply is required.

Run manually:
    sudo python3 stepper_l298n_node.py

Send a command from another terminal:
    ros2 topic pub --once /stepper_cmd std_msgs/msg/Int32 "{data: 200}"
"""

import time

import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32

try:
    import RPi.GPIO as GPIO
except ImportError:
    raise SystemExit(
        "RPi.GPIO is not installed. Run:\n"
        "    sudo apt update\n"
        "    sudo apt install -y python3-rpi.gpio\n"
        "or:\n"
        "    sudo pip3 install RPi.GPIO"
    )

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
IN1, IN2, IN3, IN4 = 17, 18, 27, 22   # BCM pin numbers
STEP_DELAY = 0.003                     # seconds between steps (lower = faster)

FULL_STEP_SEQUENCE = [
    (1, 0, 1, 0),
    (0, 1, 1, 0),
    (0, 1, 0, 1),
    (1, 0, 0, 1),
]

class StepperNode(Node):
    def __init__(self):
        super().__init__('motor_driver')

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        for pin in (IN1, IN2, IN3, IN4):
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW)

        self._seq_index = 0

        self.subscription = self.create_subscription(
            Int32,
            'stepper_cmd',
            self.stepper_cmd_callback,
            10
        )
        self.get_logger().info(
            'Stepper node ready. Publish an Int32 to /stepper_cmd '
            '(positive = CW steps, negative = CCW steps).'
        )

    def set_pins(self, state):
        GPIO.output(IN1, state[0])
        GPIO.output(IN2, state[1])
        GPIO.output(IN3, state[2])
        GPIO.output(IN4, state[3])

    def release(self):
        self.set_pins((0, 0, 0, 0))

    def stepper_cmd_callback(self, msg: Int32):
        steps = msg.data
        direction = 1 if steps >= 0 else -1
        steps = abs(steps)

        self.get_logger().info(
            f'Rotating {steps} steps {"CW" if direction == 1 else "CCW"}'
        )

        seq_len = len(FULL_STEP_SEQUENCE)
        for _ in range(steps):
            self._seq_index = (self._seq_index + direction) % seq_len
            self.set_pins(FULL_STEP_SEQUENCE[self._seq_index])
            time.sleep(STEP_DELAY)

        self.release()

    def destroy_node(self):
        self.release()
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