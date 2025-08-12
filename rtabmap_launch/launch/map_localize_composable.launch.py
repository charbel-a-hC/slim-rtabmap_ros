import os
import launch
import launch_ros.actions
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
from launch.actions import DeclareLaunchArgument
from launch.actions import TimerAction

def generate_launch_description():
    # Arguments
    mapping_config_path = 'src/visual_localization/rtabmap_launch/config/mapping.ini'
    database_path = "/ros2_ws/rtabmap.db"
    
    declare_args = [
        # Basic arguments
        DeclareLaunchArgument('stereo', default_value='false', description='Use stereo input instead of RGB-D.'),
        DeclareLaunchArgument('localization', default_value='false', description='Launch in localization mode.'),
        DeclareLaunchArgument('rtabmap_viz', default_value='true', description='Launch RTAB-Map UI (optional).'),
        DeclareLaunchArgument('rviz', default_value='false', description='Launch RVIZ (optional).'),
        DeclareLaunchArgument('use_sim_time', default_value='false', description='Use simulation (Gazebo) clock if true'),
        DeclareLaunchArgument('log_level', default_value='info', description='ROS logging level (debug, info, warn, error).'),

        # Config files
        DeclareLaunchArgument('cfg', default_value='', description='To change RTAB-Map\'s parameters, set the path of config file (*.ini).'),
        DeclareLaunchArgument('gui_cfg', default_value='~/.ros/rtabmap_gui.ini', description='Configuration path of rtabmap_viz.'),
        DeclareLaunchArgument('rviz_cfg', default_value='', description='Configuration path of rviz2.'),

        # Frame settings
        DeclareLaunchArgument('frame_id', default_value='base_link', description='Fixed frame id of the robot (base frame).'),
        DeclareLaunchArgument('odom_frame_id', default_value='', description='If set, TF is used to get odometry instead of the topic.'),
        DeclareLaunchArgument('map_frame_id', default_value='map', description='Output map frame id (TF).'),
        DeclareLaunchArgument('map_topic', default_value='map', description='Map topic name.'),
        DeclareLaunchArgument('publish_tf_map', default_value='true', description='Publish TF between map and odometry.'),
        DeclareLaunchArgument('namespace', default_value='rtabmap', description=''),
        DeclareLaunchArgument('database_path', default_value='~/.ros/rtabmap.db', description='Where is the map saved/loaded.'),

        # Queue and synchronization
        DeclareLaunchArgument('topic_queue_size', default_value='1', description='Queue size of subscribers.'),
        DeclareLaunchArgument('queue_size', default_value='10', description='Queue size'),
        DeclareLaunchArgument('qos', default_value='1', description='QoS level'),
        DeclareLaunchArgument('wait_for_transform', default_value='0.2', description=''),
        DeclareLaunchArgument('approx_sync', default_value='false', description='If timestamps of the input topics should be synchronized using approximate or exact time policy.'),
        DeclareLaunchArgument('approx_sync_max_interval', default_value='0.0', description='(sec) 0 means infinite interval duration (used with approx_sync=true)'),

        # RGB-D topics
        DeclareLaunchArgument('rgb_topic', default_value='/camera/rgb/image_rect_color', description=''),
        DeclareLaunchArgument('depth_topic', default_value='/camera/depth_registered/image_raw', description=''),
        DeclareLaunchArgument('camera_info_topic', default_value='/camera/rgb/camera_info', description=''),

        # Stereo topics
        DeclareLaunchArgument('stereo_namespace', default_value='/stereo_camera', description=''),
        DeclareLaunchArgument('left_image_topic', default_value='', description=''),
        DeclareLaunchArgument('right_image_topic', default_value='', description=''),
        DeclareLaunchArgument('left_camera_info_topic', default_value='', description=''),
        DeclareLaunchArgument('right_camera_info_topic', default_value='', description=''),

        # RGBD sync
        DeclareLaunchArgument('rgbd_sync', default_value='false', description='Pre-sync rgb_topic, depth_topic, camera_info_topic.'),
        DeclareLaunchArgument('approx_rgbd_sync', default_value='true', description='false=exact synchronization'),
        DeclareLaunchArgument('subscribe_rgbd', default_value='false', description=''),
        DeclareLaunchArgument('rgbd_topic', default_value='rgbd_image', description=''),
        DeclareLaunchArgument('depth_scale', default_value='1.0', description=''),

        # Image compression
        DeclareLaunchArgument('compressed', default_value='false', description='If you want to subscribe to compressed image topics'),
        DeclareLaunchArgument('rgb_image_transport', default_value='compressed', description='Common types: compressed, theora'),
        DeclareLaunchArgument('depth_image_transport', default_value='compressedDepth', description='Depth compatible types: compressedDepth'),

        # LiDAR
        DeclareLaunchArgument('subscribe_scan', default_value='false', description=''),
        DeclareLaunchArgument('scan_topic', default_value='/scan', description=''),
        DeclareLaunchArgument('subscribe_scan_cloud', default_value='false', description=''),
        DeclareLaunchArgument('scan_cloud_topic', default_value='/scan_cloud', description=''),
        DeclareLaunchArgument('scan_normal_k', default_value='0', description=''),

        # Odometry
        DeclareLaunchArgument('visual_odometry', default_value='true', description='Launch rtabmap visual odometry node.'),
        DeclareLaunchArgument('icp_odometry', default_value='false', description='Launch rtabmap icp odometry node.'),
        DeclareLaunchArgument('odom_topic', default_value='odom', description='Odometry topic name.'),
        DeclareLaunchArgument('vo_frame_id', default_value='odom', description='Visual/ICP odometry frame ID for TF.'),
        DeclareLaunchArgument('publish_tf_odom', default_value='true', description=''),
        DeclareLaunchArgument('odom_tf_angular_variance', default_value='0.01', description='If TF is used to get odometry, this is the default angular variance'),
        DeclareLaunchArgument('odom_tf_linear_variance', default_value='0.001', description='If TF is used to get odometry, this is the default linear variance'),
        DeclareLaunchArgument('odom_args', default_value='', description='More arguments for odometry'),
        DeclareLaunchArgument('odom_sensor_sync', default_value='false', description=''),
        DeclareLaunchArgument('odom_guess_frame_id', default_value='', description=''),
        DeclareLaunchArgument('odom_guess_min_translation', default_value='0.0', description=''),
        DeclareLaunchArgument('odom_guess_min_rotation', default_value='0.0', description=''),

        # IMU
        DeclareLaunchArgument('imu_topic', default_value='/imu/data', description='Used with VIO approaches and for SLAM graph optimization.'),
        DeclareLaunchArgument('wait_imu_to_init', default_value='false', description=''),

        # User data
        DeclareLaunchArgument('subscribe_user_data', default_value='false', description='User data synchronized subscription.'),
        DeclareLaunchArgument('user_data_topic', default_value='/user_data', description=''),
        DeclareLaunchArgument('user_data_async_topic', default_value='/user_data_async', description=''),

        # GPS
        DeclareLaunchArgument('gps_topic', default_value='/gps/fix', description='GPS async subscription.'),

        # Tag/Landmark
        DeclareLaunchArgument('tag_topic', default_value='/detections', description='AprilTag topic async subscription.'),
        DeclareLaunchArgument('tag_linear_variance', default_value='0.0001', description=''),
        DeclareLaunchArgument('tag_angular_variance', default_value='9999.0', description=''),
        DeclareLaunchArgument('fiducial_topic', default_value='/fiducial_transforms', description=''),

        # Additional settings
        DeclareLaunchArgument('rtabmap_args', default_value='', description='Backward compatibility, use "args" instead.'),
        DeclareLaunchArgument('launch_prefix', default_value='', description='For debugging purpose, e.g., "xterm -e gdb -ex run --args"'),
        DeclareLaunchArgument('output', default_value='screen', description='Control node output (screen or log).'),
        DeclareLaunchArgument('initial_pose', default_value='', description='Set an initial pose (only in localization mode).'),
        DeclareLaunchArgument('output_goal_topic', default_value='/goal_pose',      description='Output goal topic (can be connected to nav2).'),
        DeclareLaunchArgument('ground_truth_frame_id',      default_value='', description='e.g., "world"'),
        DeclareLaunchArgument('ground_truth_base_frame_id', default_value='', description='e.g., "tracker", a fake frame matching the frame "frame_id" (but on different TF tree)'),
        DeclareLaunchArgument('use_action_for_goal', default_value='false',         description='Connect to nav2\'s navigate_to_pose action server instead of publishing the output goal topic.'),
        DeclareLaunchArgument('Mem/InitWMWithAllNodes', default_value='true',         description=''),
        DeclareLaunchArgument('Mem/IncrementalMemory', default_value='true',         description=''),
        
    ]

    # Create a static transform publisher node
    static_transform_publisher = launch_ros.actions.Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        arguments=['0', '0', '0', '0.0', '0.0', '0.0', '1.0', 'base_camera', 'camera'],
        name='static_transform_publisher',
        output='screen',
    )
    
    # Include the rtabmap components launch file
    rtabmap_container = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(['src/visual_localization/rtabmap_launch/include/rtabmap_composable.launch.py']),
        launch_arguments={
            'cfg': mapping_config_path,
            'database_path': database_path,
            'rtabmap_viz': 'false',
            'rviz': 'false',
            'use_sim_time': 'false',
            'approx_sync': 'true',
            'approx_sync_max_interval': '0.1',
            'wait_for_transform': '0.2',
            'Mem/IncrementalMemory': 'true',
            'Mem/InitWMWithAllNodes': 'false',
            'frame_id': 'base_footprint',
            'odom_topic': 'odom',
            'odom_frame_id': '',
            'visual_odometry': 'true',
            'rgb_topic': '/rgb_image',
            'depth_topic': '/depth_image',
            'camera_info_topic': '/color_intrinsics',
            'stereo': 'false',
            "subscribe_rgb": "true",
            "subscribe_depth": "true",
            "depth": "true"
        }.items()
    )
    
    delayed_container = TimerAction(
        period=3.0,  # 2 second delay
        actions=[rtabmap_container]
    )
    return launch.LaunchDescription([
        *declare_args,
        static_transform_publisher,
        delayed_container

    ])