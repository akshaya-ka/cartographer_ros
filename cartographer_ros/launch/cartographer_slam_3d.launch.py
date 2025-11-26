from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():

    # Initialize LaunchDescription first
    ld = LaunchDescription()

    config_dir = LaunchConfiguration("config_dir")
    config_basename = LaunchConfiguration("config_basename")
    use_sim_time = LaunchConfiguration("use_sim_time", default="false")
    use_rviz = LaunchConfiguration("use_rviz")

    # --- Arguments ---
    config_directory_arg = DeclareLaunchArgument(
        'config_dir',
        default_value='install/cartographer_ros/share/cartographer_ros/configuration_files',
        description='Cartographer config directory'
    )

    config_basename_arg = DeclareLaunchArgument(
        'config_basename',
        default_value='cartographer_slam_3d.lua',
        description='3D SLAM configuration file'
    )

    use_sim_time_arg = DeclareLaunchArgument(
        'use_sim_time',
        default_value='false',
        description='Use simulation time'
    )

    use_rviz_arg = DeclareLaunchArgument(
        'use_rviz',
        default_value='true',
        description='Whether to launch RViz'
    )

    # ---- CARTOGRAPHER NODE ----
    cartographer_node = Node(
        package='cartographer_ros',
        executable='cartographer_node',
        name='cartographer_slam_3d',
        output='screen',
        parameters=[{'use_sim_time': use_sim_time}],
        arguments=[
            '-configuration_directory', config_dir,
            '-configuration_basename', config_basename],
        remappings=[
            ('points2', '/livox/amr/lidar'),
            ('imu', '/livox/amr/imu'),
            ('odom', '/odom')]
    )

    # ---- OCCUPANCY GRID NODE (optional for 2D projection) ----
    occupancy_grid_node = Node(
        package='cartographer_ros',
        executable='cartographer_occupancy_grid_node',
        name='occupancy_grid_node',
        output='screen',
        parameters=[
            {'resolution': 0.05},
            {'publish_period_sec': 1.0},
            {'use_sim_time': use_sim_time}]
    )

    # rviz2_node = Node(
    #     package='rviz2',
    #     executable='rviz2',
    #     name='rviz2',
    #     parameters=[{'use_sim_time': use_sim_time}],
    #     condition=IfCondition(use_rviz),
    #     output='screen')

    ld.add_action(use_rviz_arg)
    ld.add_action(use_sim_time_arg)
    ld.add_action(config_directory_arg)
    ld.add_action(config_basename_arg)
    ld.add_action(cartographer_node)
    ld.add_action(occupancy_grid_node)
    # ld.add_action(rviz2_node)

    return ld
