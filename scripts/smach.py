import rclpy
from rclpy.node import Node
from time import sleep
from cyberdog_msg.msg import YamlParam, ApplyForce
import lcm
from exlcm import gamepad_lcmt
import control
import laser
import rgb

import sys                                                                  
import signal
from match import match
import threading
import math
import copy


mode = 0
debug = True
debug = False



goal_cor = {
    'turn_1':[8.85,0],
    # 'turn_1':[8.5,0.2],
    'round':[8.5,3.831],
    'turn_2':[8.5,8.7],
    'turn_3' :[-0.5,8.7]
}
round = [[8,3.7],[7.87,4.3],[8.1,4.9],[8.3,5.3]]




circle_cor = []
def quit(signum, frame):
    example_node.switch_mode(12)
    print ('stop fusion')
    sys.exit()

def findAllFile(base):
    for root, ds, fs in os.walk(base):
        for f in fs:
            yield f


class ControlParameterValueKind:
    kDOUBLE = 1
    kS64 = 2
    kVEC_X_DOUBLE = 3  # for template type derivation
    kMAT_X_DOUBLE = 4  # for template type derivation

class ExampleNode(Node):

    def __init__(self, node_name):
        super().__init__(node_name)
        self.para_pub_ = self.create_publisher(YamlParam, 'yaml_parameter', 10)
        self.force_pub_ = self.create_publisher(ApplyForce, 'apply_force', 10)
        param_message_ = YamlParam()
        param_message_.name = "use_rc"
        param_message_.kind = ControlParameterValueKind.kS64
        param_message_.s64_value = 0
        param_message_.is_user = 0
        self.para_pub_.publish(param_message_)
        self.get_logger().info("Switch to gamepad control model...")
        sleep(1)



    def switch_mode(self,num):
        num = int(num)
        param_message_ = YamlParam()
        param_message_.name = "control_mode"
        param_message_.kind = ControlParameterValueKind.kS64
        param_message_.s64_value = num
        param_message_.is_user = 0
        self.para_pub_.publish(param_message_)
        
    
    def switch_id(self,num):
        num = int(num)
        param_message_ = YamlParam()
        param_message_.name = "gait_id"
        param_message_.kind = ControlParameterValueKind.kS64
        param_message_.s64_value = num
        param_message_.is_user = 0
        self.para_pub_.publish(param_message_)
        

def correct_pose_x(x):
    dis = Control.min_front_range
    print("dis", dis)
    pose = copy.deepcopy(Control._pose)
    pose[0] = x - dis
    print("pose[0]",pose[0])
    Control.correct_pose(pose)

def correct_pose_y(y):
    dis = Control.min_front_range
    print("dis", dis)
    pose = Control._pose
    pose[1] = y - dis
    print("pose[1]",pose[0])
    Control.correct_pose(pose)

#######################################################################  0
def mode0():
    global mode,goal_cor
    sleep(2)
    example_node.switch_mode(12)
    sleep(1)
    example_node.switch_id(27)
    # example_node.switch_id(26)
    example_node.switch_mode(11)
    Control.vel = 0.2
    Control.pub_vel()
    sleep(0.4)
    Control.max_vel = 0.2
    Control.goal_cor = goal_cor["turn_1"]
    mode = 1
#######################################################################  1
def mode1():
    global mode,goal_cor,debug
    Control.get_vel()
    # Control.vel = 0.2
    # Control.rotate(0)
    Control.pub_vel()
    if Control._pose[0]> 2:
        example_node.switch_id(27)
    if Control.rho < 0.6 or debug:
        
        Control.pub_vel(True)
        example_node.switch_mode(12)
        sleep(2)
        Control.correct_pose_x(10.2,0.53)
        print(Control.min_front_range)
        print(Control._pose[0])
        sleep(5)
        # correct_pose_x(9.25)
        # if Control.min_front_range > 0.5:
        #     example_node.switch_id(27)
        #     example_node.switch_mode(11)
        #     return
        
        Control.goal_cor = goal_cor["round"]
        Control.max_vel = 0.1

        example_node.switch_id(0)
        example_node.switch_mode(16)
        sleep(2)
        example_node.switch_mode(12)
        sleep(2)
        example_node.switch_id(27)
        example_node.switch_mode(11)
        Control.step_height = 0.07
        Control.correct_yaw(math.pi/2)
        mode = 2
#######################################################################  2
def mode2():
    global mode,goal_cor,debug
    Control.get_vel()
    Control.vel = 0.15
    Control.rotate(math.pi/2)
    Control.pub_vel()
    if Control.rho < 0.7 or debug:
        Control.pub_vel(True)
        Control.max_vel = 0.1
        Control.max_ang = 0.08
        Control.kp2 = 0.2
        Control.kp1 = 0.2
        example_node.switch_mode(12)
        sleep(3)
        
        # pose = Control._pose
        # pose[1] = 3.8 - Laser.front_dis - 0.1
        # Control.correct_pose(pose)
        correct_pose_y(3.8)
        # if Control.min_front_range > 0.15:
        #     example_node.switch_id(27)
        #     example_node.switch_mode(11)
        #     return
        
        example_node.switch_id(0)
        example_node.switch_mode(16)
        sleep(2)
        example_node.switch_mode(12)
        sleep(2)
        example_node.switch_id(27)
        example_node.switch_mode(11)
        Control.correct_yaw(math.pi*0.85)
        # Control.goal_cor = goal_cor["round_2"]
        # Control.vel = 0.2
        # Control.ang = -0.16
        # Control.pub_vel()
        mode = 3

#######################################################################  3
def mode3():
    global mode,goal_cor,round
    Control.rho = 1
    count = 0
    for cor in round:
        count +=1
        Control.goal_cor = cor
        Control.get_vel()
        while Control.rho > 0.25:
            print("Control.rho",Control.rho)
            print("count",count)
            Control.get_vel()
            Control.pub_vel()
        
    # Control.pub_vel(True)
    # Control.goal_cor = goal_cor["jump_1"]
    Control.max_vel = 0.2
    # example_node.switch_mode(12)
    # sleep(2)
    # example_node.switch_id(0)
    # example_node.switch_mode(16)
    example_node.switch_id(9)
    # example_node.switch_mode(11)
    Control.goal_cor = goal_cor["turn_2"]
    Control.rotate(math.pi/2)
    mode = 4
    # Control.get_vel()
    # Control.vel = 0.2
    # Control.ang = -0.16
    # Control.pub_vel()
    # if Control.rho < 0.5:
    #     example_node.switch_mode(12)
    #     sleep(2)
    #     example_node.switch_id(0)
    #     example_node.switch_mode(16)
    #     sleep(2)
    #     example_node.switch_mode(12)
    #     sleep(2)
    #     mode = 4

#######################################################################  4
def mode4():
    global mode,goal_cor,debug
    Control.get_vel()
    Control.vel = 0.2
    Control.pub_vel()
    if Control.rho < 0.5 or debug:
        # print("Control.min_front_range",Control.min_front_range)
        Control.pub_vel(True)
        example_node.switch_mode(12)
        sleep(2)
        # correct_pose_x(9.25)
        # if Control.min_front_range > 0.5:
        #     example_node.switch_id(27)
        #     example_node.switch_mode(11)
        #     return
        
        # Control.goal_cor = goal_cor["round"]
        Control.max_vel = 0.2

        example_node.switch_id(0)
        example_node.switch_mode(16)
        sleep(2)
        example_node.switch_mode(12)
        sleep(2)
        example_node.switch_id(9)
        example_node.switch_mode(11)
        Control.goal_cor = goal_cor["turn_3"]
        Control.correct_yaw(math.pi)
        mode = 5

#######################################################################  5

def mode5():
    global mode,goal_cor,debug
    Control.get_vel()
    Control.vel = 0.2
    Control.pub_vel()
    if Control.rho < 0.5 or debug:
        print("Control.min_front_range",Control.min_front_range)
        Control.pub_vel(True)
        example_node.switch_mode(12)
        sleep(2)
        example_node.switch_id(0)
        example_node.switch_mode(16)
        sleep(2)
        example_node.switch_mode(12)
        sleep(2)
        example_node.switch_mode(11)
        # sleep(2.5)
        # Control.step_height = 0.07
        # example_node.switch_id(27)
        # example_node.switch_mode(11)
        Control.correct_yaw(-math.pi/2)
        mode = 6

#######################################################################  6

def mode6():
    global mode,goal_cor,debug
    while Control._pose[1] > 1:
        Control.vel = 0.2
        Control.rotate(-math.pi/2)
        Control.pub_vel()
        # print("color_recognizer_node.is_green",color_recognizer_node.is_red)
        if Control.is_red:
            if Control.status:
                left_forward()
                Control.status = 0
            else:
                right_forward()
                Control.status = 1
    example_node.switch_mode(12)
    sleep(1)
    example_node.switch_mode(7)




def right_forward():
    Control.vel = 0.2
    Control.rotate(-math.pi/2)
    Control.pub_vel()
    sleep(3.3)
    Control.pub_vel(True)
    sleep(0.2)
    Control.pub_vel(rl=-0.2)
    sleep(7)
    
def left_forward():
    Control.vel = 0.2
    Control.rotate(-math.pi/2)
    Control.pub_vel()
    sleep(3.3)
    Control.pub_vel(True)
    sleep(0.2)
    Control.pub_vel(rl=0.2)
    sleep(7)

def ros_spin_thread(node):
    rclpy.spin(Control)


def test():
    Control.correct_yaw(math.pi/2)

def main():
    global mode
    signal.signal(signal.SIGINT, quit)                                
    signal.signal(signal.SIGTERM, quit)

    spin_thread_1 = threading.Thread(target=ros_spin_thread, args=(Control,))
    spin_thread_1.start()

    # spin_thread_2 = threading.Thread(target=ros_spin_thread, args=(Laser,))
    # spin_thread_2.start()

    # spin_thread_3 = threading.Thread(target=ros_spin_thread, args=(color_recognizer_node,))
    # spin_thread_3.start()

    while True:
        if mode == 0:
            print("mode",mode)
            #启动
            mode0()
        elif mode == 1:
            # print("mode",mode)
            #,快走至斜坡
            mode1()
        elif mode == 2:
            # print("mode",mode)
            mode2()
        elif mode == 3:
            # print("mode",mode)
            mode3()
        elif mode == 4:
            # print("mode",mode)
            mode4()
        elif mode == 5:
            # print("mode",mode)
            mode5()
        elif mode == 6:
            # print("mode",mode)
            mode6()
        else:
            print("err")


def cal_circle_cor():
    global circle_cor
    center_x = 8.5
    center_y = 3.9
    radius = 0.63

    # 步长
    step = 0.05

    # 初始x值
    y = center_y - radius

    # 存储结果的列表
    points = []

    while y  <= center_y + radius:
        # 计算y的两个可能值
        x = center_x - math.sqrt(radius**2 + (y-center_y)**2)
        
        # 添加到结果列表
        points.append((x, y))
        
        # 增加x值
        y +=step
    circle_cor = points


if __name__ == '__main__':
    rclpy.init()
    example_node = ExampleNode("cyberdogmsg_node")
    Control = control.Robot_Control()
    # Laser = laser.RadarListener()
    # color_recognizer_node = rgb.ColorRecognizerNode()
    # cal_circle_cor()
    # position_update_thread = threading.Thread(target=Control.pose)
    # position_update_thread.daemon = True
    # position_update_thread.start()
    # rclpy.spin(Control)
    main()

