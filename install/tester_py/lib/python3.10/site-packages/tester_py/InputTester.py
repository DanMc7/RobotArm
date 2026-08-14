import rclpy
import threading
from rclpy.node import Node
from std_msgs.msg import Int32MultiArray

class TerminalPublisher(Node):

    def __init__(self):
        super().__init__('terminal_publisher')
        self.publisher_ = self.create_publisher(Int32MultiArray, 'stepper_cmd', 10)
        self.input_thread = threading.Thread(target=self.input_loop, daemon=True)
        self.input_thread.start()

    def input_loop(self):
        while rclpy.ok():
            user_input = input("Enter steps and millisecond step delay (Format: xx xx): ")
            extractedNumbers = user_input.split()
            output = [int(x) for x in extractedNumbers]
            msg = Int32MultiArray()
            msg.data = output
            self.publisher_.publish(msg)
            self.get_logger().info(f'Published: "{msg.data}"')

def main(args=None):
    rclpy.init(args=args)
    terminal_publisher = TerminalPublisher()
    rclpy.spin(terminal_publisher)
    terminal_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()