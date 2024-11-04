import rclpy
from rclpy.node import Node
from tf2_ros import Buffer, TransformListener
from geometry_msgs.msg import TransformStamped, PoseStamped, PointStamped
from quaternions import Quaternion as Quaternion
from math import cos,sin,atan2,pi
import numpy as np
from exlcm import gamepad_lcmt
import lcm
from rclpy.qos import QoSProfile, QoSReliabilityPolicy
from sensor_msgs.msg import LaserScan,Image
import time

class Robot_Control(Node):

    def __init__(self):
        super().__init__('robot_transform_listener')
        qos_profile = QoSProfile(
            depth=10,
            reliability=QoSReliabilityPolicy.BEST_EFFORT
        )
        self.min_front_range = 0
        self.subscription = self.create_subscription(
            LaserScan,
            '/scan',
            self.listener_callback,
            qos_profile)

        self.subscription_2 = self.create_subscription(
            Image,
            '/rgb_camera/image_raw',
            self.image_callback,
            qos_profile)
        
        self.is_green = False
        self.is_red = True
        self.status = 1 # 1:right 0:left

        self.subscription  # prevent unused variable warning
        self.lc = lcm.LCM()

        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        # self.pose_publisher = self.create_publisher(PoseStamped, '/pose', 10)
        self.timer = self.create_timer(0.01, self.timer_callback)
        self.timer2 = self.create_timer(0.5, self.cor_pub)
        self._pose = [0,0,0] #x,y,yaw
        self.kp1 = 0.08
        self.kp2 = 0.1
        self.max_vel = 0.2
        self.max_ang = 0.1
        self.vel = 0
        self.ang = 0
        self.step_height = 0.11
        self.goal_cor = [0,0]
        self.rho = 0
        diff_theta = 0
        self.range = []

        self.correct_x = 0
        self.correct_y = 0
        self.correct_th = 0

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
            # print("r",r,"g",g,"b",b)
            # print("is_green",is_green)
            if is_green:
                self.is_green = True
                self.is_red = False
            else:
                self.is_green = False
                self.is_red = True

        except Exception as e:
            self.get_logger().error(f"处理图像时发生错误: {e}")

    def listener_callback(self, msg):
        # msg = LaserScan()
        # angle_increment = msg.angle_increment
        # min_range = 
        self.range = msg.ranges
        self.min_front_range = min(msg.ranges[85:95])
        # print(msg._range_min)
        # print(msg._range_max)


    def get_vel(self):
        x_diff = self.goal_cor[0] - self._pose[0]
        y_diff = self.goal_cor[1] - self._pose[1]
        # print("goal_cor[0]",self.goal_cor[0],"self._pose[0]",self._pose[0])
        theta = atan2(y_diff, x_diff)
        # print("theta",theta,"self._pose[2]",self._pose[2])
        theta = theta - self._pose[2]
        dis = np.hypot(x_diff, y_diff)
        if theta < -pi:
            theta += 2*pi
        elif theta > pi:
            theta -= 2*pi
        self.diff_theta = theta
        # print("dis",dis,"theta",theta)
        self.rho = dis

        self.vel = self.kp1 * dis
        self.vel = self.vel if self.vel < self.max_vel else self.max_vel
        self.ang = self.kp2 * theta
        self.ang = self.ang if abs(self.ang)< self.max_ang else np.sign(self.ang)*self.max_ang
        # print("self.vel",self.vel,"self.ang",self.ang)
        

    def rotate(self,theta):
        # print("theta",theta,"self._pose[2]",self._pose[2])
        theta = theta - self._pose[2]
        if theta < -pi:
            theta += 2*pi
        elif theta > pi:
            theta -= 2*pi
        self.diff_theta = theta
        self.ang = self.kp2 * theta
        self.ang = self.ang if abs(self.ang)< self.max_ang else np.sign(self.ang)*self.max_ang
        # print("self.vel",self.vel,"self.ang",self.ang)

    def correct_yaw(self,theta):
        self.rotate(theta)
        while (abs(self.diff_theta) > 0.08) :
            print("diff_yaw",abs(self.diff_theta))
            self.rotate(theta)
            self.vel = 0
            self.pub_vel()

    def timer_callback(self):
        try:
            transform: TransformStamped = self.tf_buffer.lookup_transform(
                'vodom', 'base_link', rclpy.time.Time())
            self._pose[0] = transform.transform.translation.x + self.correct_x
            self._pose[1] = transform.transform.translation.y + self.correct_y
            self._pose[2] = Quaternion.get_euler(transform.transform.rotation)[2] + self.correct_th
            # 发布PoseStamped消息
            # self.get_logger().info(f"Published pose: {self._pose}")
        except Exception as e:
            self.get_logger().warn(f"Could not transform: {str(e)}")
            
    def cor_pub(self):
        if self._pose:
            # print("x",self._pose[0])
            # print("y",self._pose[1])
            # print("z",self._pose[2])
            # print("laser",self.min_front_range)
            # print("rho",self.rho)
            pass

    # def correct_pose(self,pose):
    #     self.correct_x =  pose[0] - self._pose[0] 
    #     self.correct_y =  pose[1] - self._pose[1]
    #     self.correct_th = pose[2] - self._pose[2]
    #     print("self.correct_x",self.correct_x)
    #     print("self.correct_y",self.correct_y)
    #     print("self.correct_th",self.correct_th)
    def correct_pose_x(self,std_x,std):
        self.correct_x =  (std_x-std) - self._pose[0] 
        print("self.correct_x",self.correct_x)
        print("self.min_front_range",self.min_front_range)
        print("std",std)
        err = self.min_front_range - std
        self.vel = 0.1 * np.sign(err)
        self.ang = 0
        self.pub_vel()
        tt = abs(err)/0.05
        time.sleep(tt)



    def pub_vel(self,flag=False,rl = 0):
        gamepad_lcm_type = gamepad_lcmt()
        gamepad_lcm_type.rightTriggerAnalog = self.step_height
        if flag:
            self.vel = 0
            self.ang = 0
            gamepad_lcm_type.leftStickAnalog[1] = 0
            gamepad_lcm_type.leftStickAnalog[0] = 0
            gamepad_lcm_type.leftTriggerAnalog= 0
        else:
            gamepad_lcm_type.leftStickAnalog[0] = self.vel
            gamepad_lcm_type.leftStickAnalog[1] = rl
            gamepad_lcm_type.leftTriggerAnalog= self.ang
        self.lc.publish("gamepad_lcmt", gamepad_lcm_type.encode())

# def main(args=None):
#     rclpy.init(args=args)
#     node = Robot_Control()
#     try:
#         rclpy.spin(node)
#     except KeyboardInterrupt:
#         pass
#     finally:
#         node.destroy_node()
#         rclpy.shutdown()

# if __name__ == '__main__':
#     main()
