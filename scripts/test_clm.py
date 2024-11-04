import rclpy
from rclpy.node import Node
from time import sleep
from cyberdog_msg.msg import YamlParam
import lcm
from exlcm import gamepad_lcmt
from smach import ExampleNode

class ControlParameterValueKind:
    kDOUBLE = 1
    kS64 = 2
    kVEC_X_DOUBLE = 3  # for template type derivation
    kMAT_X_DOUBLE = 4  # for template type derivation

# class ExampleNode(Node):
#     def __init__(self, node_name):
#         super().__init__(node_name)
#         self.para_pub_ = self.create_publisher(YamlParam, 'yaml_parameter', 10)

#     def send_control_mode(self):
#         param_message_ = YamlParam()
        
#         sleep(1)
#         param_message_.name = "use_rc"
#         param_message_.kind = ControlParameterValueKind.kS64
#         param_message_.s64_value = 0
#         param_message_.is_user = 0
#         self.para_pub_.publish(param_message_)
#         self.get_logger().info("Switch to gamepad control model...")

def main(args=None):
    rclpy.init(args=args)
    example_node = ExampleNode("kdcommand_node")
    key = input("id ")
    example_node.switch_id(int(key))
    # example_node.switch_mode(62)
    # sleep(15)
    print(1)
    rclpy.shutdown()

    # Initialize LCM
    lc = lcm.LCM()

    gamepad_lcm_type = gamepad_lcmt()
    key = ''
    gamepad_lcm_type.rightTriggerAnalog = 0.06
    while True:
        key = input("Type command: ")
        if key == 'w':  # x direction speed
            if gamepad_lcm_type.leftStickAnalog[0] < 0.9:
                gamepad_lcm_type.leftStickAnalog[0] += 0.1
        elif key == 's':  # x direction speed
            if gamepad_lcm_type.leftStickAnalog[0] > -0.9:
                gamepad_lcm_type.leftStickAnalog[0] -= 0.1
        elif key == 'a':  # yaw direction speed
            if gamepad_lcm_type.leftStickAnalog[1] < 0.9:
                gamepad_lcm_type.leftStickAnalog[1] += 0.1
        elif key == 'd':  # yaw direction speed
            if gamepad_lcm_type.leftStickAnalog[1] > -0.9:
                gamepad_lcm_type.leftStickAnalog[1] -= 0.1
        elif key == 'j':  # yaw direction speed
            if gamepad_lcm_type.leftTriggerAnalog < 0.9:
                gamepad_lcm_type.leftTriggerAnalog += 0.1
        elif key == 'l':  # yaw direction speed
            if gamepad_lcm_type.leftTriggerAnalog > -0.9:
                gamepad_lcm_type.leftTriggerAnalog -= 0.1
        elif key == 'e':  # QP stand
            gamepad_lcm_type.x = 1
        elif key == 'r':  # locomotion
            gamepad_lcm_type.y = 1
        elif key == 't':  # pure damper
            gamepad_lcm_type.a = 1
        elif key == 'y':  # recoverystand
            gamepad_lcm_type.b = 1
        elif key == 'c':  # clear speed of all direction
            gamepad_lcm_type.leftStickAnalog[0] = 0
            gamepad_lcm_type.leftStickAnalog[1] = 0
            gamepad_lcm_type.leftTriggerAnalog = 0

        # Publish LCM message
        lc.publish("gamepad_lcmt", gamepad_lcm_type.encode())

        # Clear button states
        gamepad_lcm_type.x = 0
        gamepad_lcm_type.y = 0
        gamepad_lcm_type.a = 0
        gamepad_lcm_type.b = 0

if __name__ == '__main__':
    main()
