from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, PythonExpression
from launch_ros.actions import Node
from launch_ros.actions import SetParameter
from typing import Text
from launch_ros.actions import ComposableNodeContainer
from launch_ros.descriptions import ComposableNode    

def generate_launch_description():
    # Declare all your launch arguments here
    depth_arg = DeclareLaunchArgument(
        'depth',
        default_value=PythonExpression([
            "'true' if '", LaunchConfiguration('stereo'), "' == 'true' else 'false'"
        ]),
        description=''
    )
    
    subscribe_rgb_arg = DeclareLaunchArgument(
        'subscribe_rgb',
        default_value=LaunchConfiguration('depth'),
        description=''
    )
    
    args_arg = DeclareLaunchArgument(
        'args',
        default_value=LaunchConfiguration('rtabmap_args'),
        description='Can be used to pass RTAB-Map\'s parameters or other flags like --udebug and --delete_db_on_start/-d'
    )
    
    sync_queue_size_arg = DeclareLaunchArgument(
        'sync_queue_size',
        default_value=LaunchConfiguration('queue_size'),
        description='Queue size of topic synchronizers.'
    )
    
    # QoS arguments
    qos_image_arg = DeclareLaunchArgument(
        'qos_image',
        default_value=LaunchConfiguration('qos'),
        description='Specific QoS used for image input data: 0=system default, 1=Reliable, 2=Best Effort.'
    )
    
    qos_camera_info_arg = DeclareLaunchArgument(
        'qos_camera_info',
        default_value=LaunchConfiguration('qos'),
        description='Specific QoS used for camera info input data: 0=system default, 1=Reliable, 2=Best Effort.'
    )
    
    qos_scan_arg = DeclareLaunchArgument(
        'qos_scan',
        default_value=LaunchConfiguration('qos'),
        description='Specific QoS used for scan input data: 0=system default, 1=Reliable, 2=Best Effort.'
    )
    
    qos_odom_arg = DeclareLaunchArgument(
        'qos_odom',
        default_value=LaunchConfiguration('qos'),
        description='Specific QoS used for odometry input data: 0=system default, 1=Reliable, 2=Best Effort.'
    )
    
    qos_user_data_arg = DeclareLaunchArgument(
        'qos_user_data',
        default_value=LaunchConfiguration('qos'),
        description='Specific QoS used for user input data: 0=system default, 1=Reliable, 2=Best Effort.'
    )
    
    qos_imu_arg = DeclareLaunchArgument(
        'qos_imu',
        default_value=LaunchConfiguration('qos'),
        description='Specific QoS used for imu input data: 0=system default, 1=Reliable, 2=Best Effort.'
    )
    
    qos_gps_arg = DeclareLaunchArgument(
        'qos_gps',
        default_value=LaunchConfiguration('qos'),
        description='Specific QoS used for gps input data: 0=system default, 1=Reliable, 2=Best Effort.'
    )
    
    odom_log_level_arg = DeclareLaunchArgument(
        'odom_log_level',
        default_value=LaunchConfiguration('log_level'),
        description='Specific ROS logger level for odometry node.'
    )
    
    # Topic relay arguments using PythonExpression for the conditional concatenation
    rgb_topic_relay_arg = DeclareLaunchArgument(
        'rgb_topic_relay',
        default_value=PythonExpression([
            "str('", LaunchConfiguration('rgb_topic'), "') + '_relay' if '",
            LaunchConfiguration('compressed'), "' == 'true' else str('",
            LaunchConfiguration('rgb_topic'), "')"
        ]),
        description='Should not be modified manually!'
    )
    
    depth_topic_relay_arg = DeclareLaunchArgument(
        'depth_topic_relay',
        default_value=PythonExpression([
            "str('", LaunchConfiguration('depth_topic'), "') + '_relay' if '",
            LaunchConfiguration('compressed'), "' == 'true' else str('",
            LaunchConfiguration('depth_topic'), "')"
        ]),
        description='Should not be modified manually!'
    )
    
    left_image_topic_relay_arg = DeclareLaunchArgument(
        'left_image_topic_relay',
        default_value=PythonExpression([
            "str('", LaunchConfiguration('left_image_topic'), "') + '_relay' if '",
            LaunchConfiguration('compressed'), "' == 'true' else str('",
            LaunchConfiguration('left_image_topic'), "')"
        ]),
        description='Should not be modified manually!'
    )
    
    right_image_topic_relay_arg = DeclareLaunchArgument(
        'right_image_topic_relay',
        default_value=PythonExpression([
            "str('", LaunchConfiguration('right_image_topic'), "') + '_relay' if '",
            LaunchConfiguration('compressed'), "' == 'true' else str('",
            LaunchConfiguration('right_image_topic'), "')"
        ]),
        description='Should not be modified manually!'
    )
    
    rgbd_topic_relay_arg = DeclareLaunchArgument(
        'rgbd_topic_relay',
        default_value=PythonExpression([
            "str('", LaunchConfiguration('rgbd_topic'), "') + '_relay' if '",
            LaunchConfiguration('rgbd_sync'), "' == 'true' else str('",
            LaunchConfiguration('rgbd_topic'), "')"
        ]),
        description='Should not be modified manually!'
    )
    
    
    container = ComposableNodeContainer(
        name='rtabmap_container',
        namespace=LaunchConfiguration('namespace'),
        package='rclcpp_components',
        executable='component_container',
        composable_node_descriptions=[            
            # # RGBD Sync node
            # ComposableNode(
            #     package='rtabmap_sync',
            #     plugin='rtabmap_sync::RGBDSync',
            #     name='rgbd_sync',
            #     condition=IfCondition(PythonExpression(["'", LaunchConfiguration('stereo'), "' != 'true' and '", LaunchConfiguration('rgbd_sync'), "' == 'true'"])),
            #     parameters=[{
            #         "approx_sync": LaunchConfiguration('approx_rgbd_sync'),
            #         "approx_sync_max_interval": LaunchConfiguration('approx_sync_max_interval'),
            #         "topic_queue_size": LaunchConfiguration('topic_queue_size'),
            #         "sync_queue_size": LaunchConfiguration('sync_queue_size'),
            #         "qos": LaunchConfiguration('qos_image'),
            #         "qos_camera_info": LaunchConfiguration('qos_camera_info'),
            #         "depth_scale": LaunchConfiguration('depth_scale')
            #     }],
            #     remappings=[
            #         ("rgb/image", LaunchConfiguration('rgb_topic_relay')),
            #         ("depth/image", LaunchConfiguration('depth_topic_relay')),
            #         ("rgb/camera_info", LaunchConfiguration('camera_info_topic')),
            #         ("rgbd_image", LaunchConfiguration('rgbd_topic_relay'))
            #     ]
            # ),

            # RTAB-Map main node
            ComposableNode(
                package='rtabmap_slam',
                plugin='rtabmap_slam::CoreWrapper',
                name='rtabmap_slam',
                remappings=[
                    ("map", LaunchConfiguration('map_topic')),
                    ("rgb/image", LaunchConfiguration('rgb_topic_relay')),
                    ("depth/image", LaunchConfiguration('depth_topic_relay')),
                    ("rgb/camera_info", LaunchConfiguration('camera_info_topic')),
                    ("rgbd_image", LaunchConfiguration('rgbd_topic_relay')),
                    # ("left/image_rect", LaunchConfiguration('left_image_topic_relay')),
                    # ("right/image_rect", LaunchConfiguration('right_image_topic_relay')),
                    # ("left/camera_info", LaunchConfiguration('left_camera_info_topic')),
                    # ("right/camera_info", LaunchConfiguration('right_camera_info_topic')),
                    ("scan", LaunchConfiguration('scan_topic')),
                    ("scan_cloud", LaunchConfiguration('scan_cloud_topic')),
                    ("user_data", LaunchConfiguration('user_data_topic')),
                    ("user_data_async", LaunchConfiguration('user_data_async_topic')),
                    ("gps/fix", LaunchConfiguration('gps_topic')),
                    ("tag_detections", LaunchConfiguration('tag_topic')),
                    ("fiducial_transforms", LaunchConfiguration('fiducial_topic')),
                    ("odom", LaunchConfiguration('odom_topic')),
                    ("imu", LaunchConfiguration('imu_topic')),
                    ("goal_out", LaunchConfiguration('output_goal_topic'))],
                parameters=[{
                    "subscribe_depth": LaunchConfiguration('depth'),
                    "subscribe_rgbd": LaunchConfiguration('subscribe_rgbd'),
                    "subscribe_rgb": LaunchConfiguration('subscribe_rgb'),
                    "subscribe_stereo": LaunchConfiguration('stereo'),
                    "subscribe_scan": LaunchConfiguration('subscribe_scan'),
                    "subscribe_scan_cloud": LaunchConfiguration('subscribe_scan_cloud'),
                    "subscribe_user_data": LaunchConfiguration('subscribe_user_data'),
                    "subscribe_odom_info": PythonExpression(["'true' if ('", LaunchConfiguration('icp_odometry'), "' == 'true' or '", LaunchConfiguration('visual_odometry'), "' == 'true') else 'false'"]),
                    "ground_truth_frame_id": LaunchConfiguration('ground_truth_frame_id'),
                    "ground_truth_base_frame_id": LaunchConfiguration('ground_truth_base_frame_id'),
                    "config_path": LaunchConfiguration('cfg'),
                    # "Mem/IncrementalMemory": PythonExpression(["'true' if '", LaunchConfiguration('localization'), "' != 'true' else 'false'"]),
                    "Mem/IncrementalMemory": 'true',
                    # "Mem/InitWMWithAllNodes": PythonExpression(["'true' if '", LaunchConfiguration('localization'), "' == 'true' else 'false'"]),
                    "Mem/InitWMWithAllNodes": 'true',
                    "frame_id": LaunchConfiguration('frame_id'),
                    "map_frame_id": LaunchConfiguration('map_frame_id'),
                    "odom_frame_id": LaunchConfiguration('odom_frame_id'),
                    "publish_tf": LaunchConfiguration('publish_tf_map'),
                    "initial_pose": LaunchConfiguration('initial_pose'),
                    "use_action_for_goal": LaunchConfiguration('use_action_for_goal'),
                    "odom_tf_angular_variance": LaunchConfiguration('odom_tf_angular_variance'),
                    "odom_tf_linear_variance": LaunchConfiguration('odom_tf_linear_variance'),
                    "odom_sensor_sync": LaunchConfiguration('odom_sensor_sync'),
                    "wait_for_transform": LaunchConfiguration('wait_for_transform'),
                    "database_path": LaunchConfiguration('database_path'),
                    "approx_sync": LaunchConfiguration('approx_sync'),
                    "topic_queue_size": LaunchConfiguration('topic_queue_size'),
                    "sync_queue_size": LaunchConfiguration('sync_queue_size'),
                    "qos_image": LaunchConfiguration('qos_image'),
                    "qos_scan": LaunchConfiguration('qos_scan'),
                    "qos_odom": LaunchConfiguration('qos_odom'),
                    "qos_camera_info": LaunchConfiguration('qos_camera_info'),
                    "qos_imu": LaunchConfiguration('qos_imu'),
                    "qos_gps": LaunchConfiguration('qos_gps'),
                    "qos_user_data": LaunchConfiguration('qos_user_data'),
                    "scan_normal_k": LaunchConfiguration('scan_normal_k'),
                    "landmark_linear_variance": LaunchConfiguration('tag_linear_variance'),
                    "landmark_angular_variance": LaunchConfiguration('tag_angular_variance'),
                }],
                # arguments=[LaunchConfiguration("args"), "--ros-args", "--log-level", [LaunchConfiguration('namespace'), '.rtabmap:=', LaunchConfiguration('log_level')], "--log-level", ['rtabmap:=', LaunchConfiguration('log_level')]],
                # prefix=LaunchConfiguration('launch_prefix'),
                namespace=LaunchConfiguration('namespace')
            ),
            # Visual Odometry node
            ComposableNode(
                package='rtabmap_odom',
                plugin='rtabmap_odom::RGBDOdometry',
                name='rgbd_odometry',
                # condition=IfCondition(PythonExpression(["'", LaunchConfiguration('icp_odometry'), "' != 'true' and '", LaunchConfiguration('visual_odometry'), "' == 'true' and '", LaunchConfiguration('stereo'), "' != 'true'"])),
                parameters=[{
                    "frame_id": LaunchConfiguration('frame_id'),
                    "odom_frame_id": LaunchConfiguration('vo_frame_id'),
                    "publish_tf": LaunchConfiguration('publish_tf_odom'),
                    "ground_truth_frame_id": LaunchConfiguration('ground_truth_frame_id'),
                    "ground_truth_base_frame_id": LaunchConfiguration('ground_truth_base_frame_id'),
                    "config_path": LaunchConfiguration('cfg'),
                    "guess_frame_id": LaunchConfiguration('odom_guess_frame_id'),
                    "wait_for_transform": LaunchConfiguration('wait_for_transform'),
                    "wait_imu_to_init": LaunchConfiguration('wait_imu_to_init'),
                    "approx_sync": LaunchConfiguration('approx_sync'),
                    "approx_sync_max_interval": LaunchConfiguration('approx_sync_max_interval'),
                    "topic_queue_size": LaunchConfiguration('topic_queue_size'),
                    "sync_queue_size": LaunchConfiguration('sync_queue_size'),
                    "qos": LaunchConfiguration('qos_image'),
                    "qos_camera_info": LaunchConfiguration('qos_camera_info'),
                    "qos_imu": LaunchConfiguration('qos_imu'),
                    "subscribe_rgbd": LaunchConfiguration('subscribe_rgbd'),
                    "guess_min_translation": LaunchConfiguration('odom_guess_min_translation'),
                    "guess_min_rotation": LaunchConfiguration('odom_guess_min_rotation')}],
                remappings=[
                    ("rgb/image", LaunchConfiguration('rgb_topic_relay')),
                    ("depth/image", LaunchConfiguration('depth_topic_relay')),
                    ("rgb/camera_info", LaunchConfiguration('camera_info_topic')),
                    ("rgbd_image", LaunchConfiguration('rgbd_topic_relay')),
                    ("odom", LaunchConfiguration('odom_topic')),
                    ("imu", LaunchConfiguration('imu_topic'))],
                # arguments=[LaunchConfiguration("args"), LaunchConfiguration("odom_args"), "--ros-args", "--log-level", [LaunchConfiguration('namespace'), '.rgbd_odometry:=', LaunchConfiguration('odom_log_level')], "--log-level", ['rgbd_odometry:=', LaunchConfiguration('odom_log_level')]],
                # prefix=LaunchConfiguration('launch_prefix'),
                namespace=LaunchConfiguration('namespace')
            ),
        ],
        output='screen'
    )
    
    return LaunchDescription([
        # All argument declarations
        depth_arg,
        subscribe_rgb_arg,
        args_arg,
        sync_queue_size_arg,
        qos_image_arg,
        qos_camera_info_arg,
        qos_scan_arg,
        qos_odom_arg,
        qos_user_data_arg,
        qos_imu_arg,
        qos_gps_arg,
        odom_log_level_arg,
        rgb_topic_relay_arg,
        depth_topic_relay_arg,
        left_image_topic_relay_arg,
        right_image_topic_relay_arg,
        rgbd_topic_relay_arg,
        
        # Global parameter
        SetParameter(name='use_sim_time', value=LaunchConfiguration('use_sim_time')),
        container
    ])
