import rclpy
from rclpy.node import Node
from time import sleep
from cyberdog_msg.msg import YamlParam, ApplyForce
import lcm
from exlcm import gamepad_lcmt
from robot_control_cmd_lcmt import robot_control_cmd_lcmt
import toml
import sys
import os

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
        
        sleep(1)
        
        param_message_.name = "control_mode"
        param_message_.kind = ControlParameterValueKind.kS64
        param_message_.s64_value = num
        param_message_.is_user = 0
        self.para_pub_.publish(param_message_)
        self.get_logger().info("Recovery stand...")
    
    def switch_id(self,num):
        num = int(num)
        param_message_ = YamlParam()
        param_message_.name = "gait_id"
        param_message_.kind = ControlParameterValueKind.kS64
        param_message_.s64_value = num
        param_message_.is_user = 0
        self.para_pub_.publish(param_message_)
        self.get_logger().info("Recovery stand...")





def toml_test():
    base='/home/a_scripts/toml_/'
    num=0
    filelist=[]
    for i in findAllFile(base):
        filelist.append(i)
        print(str(num)+","+str(filelist[num]))
        num=num+1
    print('Input a toml ctrl file number:')
    numInput=int(input())
     
    lc=lcm.LCM("udpm://239.255.76.67:7671?ttl=255")
    msg=robot_control_cmd_lcmt()
    file = os.path.join(base,filelist[numInput])
    print("Load file=%s\n" % file)
    try:
        steps = toml.load(file)
        for step in steps['step']:
            msg.mode = step['mode']
            msg.value = step['value']
            msg.contact = step['contact']
            msg.gait_id = step['gait_id']
            msg.duration = step['duration']
            msg.life_count += 1
            for i in range(3):
                msg.vel_des[i] = step['vel_des'][i]
                msg.rpy_des[i] = step['rpy_des'][i]
                msg.pos_des[i] = step['pos_des'][i]
                msg.acc_des[i] = step['acc_des'][i]
                msg.acc_des[i+3] = step['acc_des'][i+3]
                msg.foot_pose[i] = step['foot_pose'][i]
                msg.ctrl_point[i] = step['ctrl_point'][i]
            for i in range(2):
                msg.step_height[i] = step['step_height'][i]

            lc.publish("robot_control_cmd",msg.encode())
            print('robot_control_cmd lcm publish mode :',msg.mode , "gait_id :",msg.gait_id , "msg.duration=" , msg.duration)
            sleep( 0.1 )
        for i in range(300): #60s Heat beat, maintain the heartbeat when life count is not updated
            lc.publish("robot_control_cmd",msg.encode())
            sleep( 0.2 )
    except KeyboardInterrupt:
        msg.mode = 7 #PureDamper before KeyboardInterrupt:
        msg.gait_id = 0
        msg.duration = 0
        msg.life_count += 1
        lc.publish("robot_control_cmd",msg.encode())
        pass
    sys.exit()

def toml_test01():

    lc=lcm.LCM()
    msg=robot_control_cmd_lcmt()
    msg.mode = 12
    msg.value = 0
    msg.contact = 0
    msg.gait_id = 0
    msg.duration = 0
    msg.life_count += 1
    for i in range(3):
        msg.vel_des[i] = 0
        msg.rpy_des[i] = 0
        msg.pos_des[i] = 0
        msg.acc_des[i] = 0
        msg.acc_des[i+3] =0
        msg.foot_pose[i] = 0
        msg.ctrl_point[i] = 0
    for i in range(2):
        msg.step_height[i] = 0
    lc.publish("robot_control_cmd",msg.encode())
    print('robot_control_cmd lcm publish mode :',msg.mode , "gait_id :",msg.gait_id , "msg.duration=" , msg.duration)
    sleep( 1 )

def main():
    # id = input("Type id: ")
    # mode = input("Type mode: ")

    example_node.switch_mode(12)
    sleep(2)

    example_node.switch_id(26)
    example_node.switch_mode(11)
    
    
    # example_node.switch_id(1)
    # example_node.switch_mode(16)

    # sleep(1.5)
    
    # example_node.switch_id(27)
    # example_node.switch_mode(11)

    example_node.destroy_node()
    rclpy.shutdown()



if __name__ == '__main__':
    rclpy.init()
    example_node = ExampleNode("cyberdogmsg_node")
    main()

'''

def findAllFile(base):
    for root, ds, fs in os.walk(base):
        for f in fs:
            yield f

def main():
    base='./'
    num=0
    filelist=[]
    for i in findAllFile(base):
        filelist.append(i)
        print(str(num)+","+str(filelist[num]))
        num=num+1
    print('Input a toml ctrl file number:')
    numInput=int(input())

    lc=lcm.LCM("udpm://239.255.76.67:7671?ttl=255")
    msg=robot_control_cmd_lcmt()
    file = os.path.join(base,filelist[numInput])
    print("Load file=%s\n" % file)
    try:
        steps = toml.load(file)
        for step in steps['step']:
            msg.mode = step['mode']
            msg.value = step['value']
            msg.contact = step['contact']
            msg.gait_id = step['gait_id']
            msg.duration = step['duration']
            msg.life_count += 1
            for i in range(3):
                msg.vel_des[i] = step['vel_des'][i]
                msg.rpy_des[i] = step['rpy_des'][i]
                msg.pos_des[i] = step['pos_des'][i]
                msg.acc_des[i] = step['acc_des'][i]
                msg.acc_des[i+3] = step['acc_des'][i+3]
                msg.foot_pose[i] = step['foot_pose'][i]
                msg.ctrl_point[i] = step['ctrl_point'][i]
            for i in range(2):
                msg.step_height[i] = step['step_height'][i]

            lc.publish("robot_control_cmd",msg.encode())
            print('robot_control_cmd lcm publish mode :',msg.mode , "gait_id :",msg.gait_id , "msg.duration=" , msg.duration)
            time.sleep( 0.1 )
        for i in range(300): #60s Heat beat, maintain the heartbeat when life count is not updated
            lc.publish("robot_control_cmd",msg.encode())
            time.sleep( 0.2 )
    except KeyboardInterrupt:
        msg.mode = 7 #PureDamper before KeyboardInterrupt:
        msg.gait_id = 0
        msg.duration = 0
        msg.life_count += 1
        lc.publish("robot_control_cmd",msg.encode())
        pass
    sys.exit()

# Main function
if __name__ == '__main__':
    main()
'''