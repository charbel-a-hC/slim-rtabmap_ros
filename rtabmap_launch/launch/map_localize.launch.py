import os
import launch
import launch_ros.actions
from launch.actions import ExecuteProcess, IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
from geometry_msgs.msg import TransformStamped
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    # Arguments
    mapping_config_path = 'src/visual_localization/rtabmap_launch/config/mapping.ini'
    database_path = "/ros2_ws/rtabmap.db"
    
    # Create a static transform publisher node
    static_transform_publisher = launch_ros.actions.Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        arguments=['0', '0', '0', '0.0', '0.0', '0.0', '1.0', 'base_camera', 'camera'],
        name='static_transform_publisher',
        output='screen',
    )
    

    # ROSBag config file
    qos_override_config_path = 'rtabmap_localization/config/qos_policies.yaml'

    
    rtabmap_launcher = IncludeLaunchDescription(
        PythonLaunchDescriptionSource('src/visual_localization/rtabmap_launch/include/rtabmap.launch.py'),
        launch_arguments={
            'cfg': mapping_config_path,
            'gui_cfg': mapping_config_path,
            
            "database_path": database_path,
            'rtabmap_viz': 'false',
            'rviz': 'false',
            
            'use_sim_time':'false',
            
            'approx_sync': 'true',
            # "rgbd_sync": "true",
            "approx_sync_max_interval": "0.02",
            "wait_for_transform": "0.2",
            
            "frame_id": "base_footprint",
            
            # "odom_sensor_sync": "True",
            "odom_topic": "odom",
            'odom_frame_id': '',
            
            "visual_odometry": "true",
            # RGB-D Config
            #####################################################
            'rgb_topic':'/rgb_image',
            'depth_topic':'/depth_image',
            'camera_info_topic':'/color_intrinsics',
            #####################################################
            
            # Stereo config
            'stereo': 'false',
            # 'stereo_namespace': 'camera',
            # 'left_image_topic': '/ir_left',
            # 'right_image_topic': '/ir_right',       
            # 'left_camera_info_topic': '/modified_left_ir_intrinsics', 
            # 'right_camera_info_topic': '/modified_right_ir_intrinsics', 
            #'camera_info_topic': '/modified_right_ir_intrinsics',
            #####################################################
                
        }.items(),
    )
    
    return launch.LaunchDescription([
        static_transform_publisher,        
        rtabmap_launcher,
    ])


