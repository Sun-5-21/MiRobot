import rclpy
from rclpy.node import Node
from tf2_ros import Buffer, TransformListener
from geometry_msgs.msg import TransformStamped, PoseStamped
from quaternions import Quaternion as Quaternion

class RobotTransformListener(Node):

    def __init__(self):
        super().__init__('robot_transform_listener')
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        self.pose_publisher = self.create_publisher(PoseStamped, '/pose', 10)
        self.timer = self.create_timer(0.01, self.timer_callback)

    def timer_callback(self):
        try:
            # 这里假设机器人在 "base_link" 坐标系下，你需要根据实际情况修改
            transform: TransformStamped = self.tf_buffer.lookup_transform(
                'vodom', 'base_link', rclpy.time.Time())
            
            # 创建PoseStamped消息并填充数据
            pose_msg = PoseStamped()
            pose_msg.header.stamp = self.get_clock().now().to_msg()
            pose_msg.header.frame_id = 'vodom'
            pose_msg.pose.position.x = transform.transform.translation.x
            pose_msg.pose.position.y = transform.transform.translation.y
            pose_msg.pose.position.z = transform.transform.translation.z
            pose_msg.pose.orientation = transform.transform.rotation
            yaw = Quaternion.get_euler(transform.transform.rotation)[2]

            # 发布PoseStamped消息
            self.pose_publisher.publish(pose_msg)

            print("x",pose_msg.pose.position.x)
            print("y",pose_msg.pose.position.y)
            print("yaw",yaw)
        except Exception as e:
            self.get_logger().warn(f"Could not transform: {str(e)}")

def main(args=None):
    rclpy.init(args=args)
    node = RobotTransformListener()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
