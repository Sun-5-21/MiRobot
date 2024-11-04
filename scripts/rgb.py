import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import Int8
import numpy as np
from rclpy.qos import QoSProfile, QoSReliabilityPolicy


class ColorRecognizerNode(Node):
    def __init__(self):
        super().__init__('color_recognizer_node')
        qos_profile = QoSProfile(
            depth=10,
            reliability=QoSReliabilityPolicy.BEST_EFFORT
        )
        self.subscription = self.create_subscription(
            Image,
            '/rgb_camera/image_raw',
            self.image_callback,
            qos_profile)
        self.subscription
        self.is_green = False
        self.is_red = True
        self.status = 1 # 1:right 0:left
        self.timer = self.create_timer(0.1, self.image_callback)
        print("start!")


    def image_callback(self, msg):
        try:
            # 获取图像尺寸
            height = msg.height
            width = msg.width
            channels = 3  # 三通道RGB格式

            # 计算中心像素的索引
            center_x = width // 2
            center_y = height // 2
            center_index = (center_y * width + center_x) * channels # 因为是一维数组，RGB三个顺序排列所以要乘以三

            # 获取中心像素的RGB值
            data = msg.data 
            # print(data)
            r = data[center_index]
            g = data[center_index + 1]
            b = data[center_index + 2]

            is_green = g > r and g > b
            print("r",r,"g",g,"b",b)
            print("is_green",is_green)
            if is_green:
                self.is_green = True
                self.is_red = False
            else:
                self.is_green = False
                self.is_red = True

        except Exception as e:
            self.get_logger().error(f"处理图像时发生错误: {e}")

# def main(args=None):
#     rclpy.init(args=args)
#     color_recognizer_node = ColorRecognizerNode()
#     rclpy.spin(color_recognizer_node)
#     color_recognizer_node.destroy_node()
#     rclpy.shutdown()

# if __name__ == '__main__':
#     main()