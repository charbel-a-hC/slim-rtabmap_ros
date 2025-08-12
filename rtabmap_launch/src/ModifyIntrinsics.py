#!/usr/bin/python3

# Fixes camera intrinsics bug in ros bridge

import rclpy
from sensor_msgs.msg import CameraInfo
from rclpy.node import Node
from functools import partial
import signal
import sys

class ModfiyIntrinsics(Node):
    def __init__(self):
        super().__init__("modify_intrinsics")
        
        topics = [
            ('/depth_intrinsics', '/modified_depth_intrinsics'),
            ('/color_intrinsics', '/modified_color_intrinsics'),
            ('/left_ir_intrinsics', '/modified_left_ir_intrinsics'),
            ('/right_ir_intrinsics', '/modified_right_ir_intrinsics'),
        ]
        
        for subscribe_topic, publish_topic in topics:
            vars(self)[f"pub_{publish_topic}"] = self.create_publisher(
                CameraInfo, publish_topic, 10
            )

            callback_func = partial(self.intrinsics_callback, sub_topic=subscribe_topic, publisher=vars(self)[f"pub_{publish_topic}"])
            
            vars(self)[f"sub_{subscribe_topic}"] = self.create_subscription(
                CameraInfo, subscribe_topic, callback_func, 10
            )
        
    def intrinsics_callback(self, msg: CameraInfo, publisher, sub_topic: str):
        # Modify the message
        modified_msg = CameraInfo()
        modified_msg.header = msg.header
        modified_msg.height = msg.height
        modified_msg.width = msg.width
        modified_msg.distortion_model = "plumb_bob"
        modified_msg.d = [0.0, 0.0, 0.0, 0.0, 0.0]
        modified_msg.r = [1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0]
        modified_msg.binning_x = msg.binning_x
        modified_msg.binning_y = msg.binning_y
        modified_msg.roi = msg.roi

        # message coming from simulation
        if msg.distortion_model == "pinhole":
            modified_msg.k, modified_msg.p = msg.k, msg.p
        else:
            modified_msg.k = [msg.k[0], 0.0, msg.k[5], 0.0, msg.k[4], msg.k[2], 0.0, 0.0, 1.0]
            modified_msg.p = [msg.k[0], 0.0, msg.k[5], 0.0, 0.0, msg.k[4], msg.k[2], 0.0, 0.0, 0.0, 1.0, 0.0] 
        
        if "right" in sub_topic:
            modified_msg.p[3] = -modified_msg.p[0]*0.055
        # Publish the modified message
        publisher.publish(modified_msg)

    def shutdown(self):
        self.shutdown_flag = True
        self.get_logger().info('Shutting down Node ...')
        self.destroy_node()

def main():
    rclpy.init()
    node = ModfiyIntrinsics()

    # Setup signal handlers
    # def signal_handler(sig, frame):
    #     node.shutdown()
    #     rclpy.shutdown()
    #     sys.exit(0)
    #
    # signal.signal(signal.SIGINT, signal_handler)
    # signal.signal(signal.SIGTERM, signal_handler)

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    # except rclpy.executors.ExternalShutdownException:
    #     node.get_logger().info('External shutdown requested')
    finally:
        node.shutdown()
        rclpy.try_shutdown()

if __name__ == '__main__':
    main()