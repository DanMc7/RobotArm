import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32
import threading

class MotorCommandPublisher(Node):

    def __init__(self):
        super().__init__('motor_command_publisher')
        self.publisher_ = self.create_publisher(Int32, 'stepper_cmd', 10)
        self.input_thread = threading.Thread(target=self.timer_callback, daemon=True)
        self.input_thread.start()

    def timer_callback(self):
        while rclpy.ok():
            output = int(input("Enter steps (positive for clockwise): "))
            msg = Int32()
            msg.data = output
            self.publisher_.publish(msg)
            self.get_logger().info(f'Published: "{msg.data}" steps.')

def main(args=None):
    rclpy.init(args=args)
    motor_command_publisher = MotorCommandPublisher()
    rclpy.spin(motor_command_publisher)
    motor_command_publisher.destroy_node()
    rclpy.shutdown()

    if __name__ == '__main__':
        main()