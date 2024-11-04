import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from rclpy.qos import QoSProfile, QoSReliabilityPolicy
from collections import deque

class RadarListener(Node):
    def __init__(self):
        super().__init__('radar_listener')
        
        # 使用 RELIABLE 策略
        qos_profile = QoSProfile(
            depth=10,
            reliability=QoSReliabilityPolicy.BEST_EFFORT
        )
        
        self.subscription = self.create_subscription(
            LaserScan,
            '/scan',
            self.listener_callback,
            qos_profile)
        self.subscription  # prevent unused variable warning

        # 滤波器窗口大小
        self.filter_window_size = 10
        self.range_buffer = deque(maxlen=self.filter_window_size)
        self.ranges = None
        self.front_dis = 0
    
    def moving_average_filter(self, ranges):
        # 将新的范围数据添加到缓冲区
        self.range_buffer.append(ranges)
        # 计算每个角度的平均值
        if len(self.range_buffer) == self.filter_window_size:
            avg_ranges = []
            for i in range(len(ranges)):
                avg_ranges.append(sum(buf[i] for buf in self.range_buffer) / self.filter_window_size)
            return avg_ranges
        else:
            return ranges

    def listener_callback(self, msg):
        # 应用移动平均滤波器
        self.ranges = self.moving_average_filter(msg.ranges)
        self.front_dis = min(msg.ranges[85:95])
        # 输出雷达的详细信息
        print(min(msg.ranges[85:95]))
