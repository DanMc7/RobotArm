import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Float32MultiArray

class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscriber_ = self.create_subscription(Float32MultiArray, 'my_topic1', self.listener_callback, 10)
        self.subscriber_

    def listener_callback(self, msg):
        self.get_logger().info('Reading: %s' % list(msg.data))

        for index, x in enumerate(msg.data):
            self.get_logger().info(f'Index: {index}  Value: {x}')

def main(args=None):
    rclpy.init(args=args)

    minimal_subscriber = MinimalSubscriber()

    rclpy.spin(minimal_subscriber)

    minimal_subscriber.destroy_node()
    rclpy.shutdown()

    if __name__ == '__main__':
        main()