#!/usr/bin/env python3

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch.substitutions import LaunchConfiguration
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch_ros.actions import Node



def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    robot_name = 'ebot_gazebo'
    world_file_name = 'task1.world'

    pkg_box_bot_gazebo = get_package_share_directory('ebot_gazebo')

    launch_file_dir = os.path.join(get_package_share_directory('ebot_gazebo'), 'launch')
    
    world = os.path.join(get_package_share_directory(robot_name), 'worlds', world_file_name)

    urdf = os.path.join(get_package_share_directory(robot_name), 'models','ebot', 'ebot.urdf')

    xml = open(urdf, 'r').read()

    xml = xml.replace('"', '\\"')
    
    swpan_args = '{name: \"my_model\", xml: \"'  +  xml + '\" }'

    spawn_node = Node(
        package="ebot_gazebo",
        executable="spawn_model",
   
    )

    return LaunchDescription([
        ExecuteProcess(
            cmd=['gazebo', '--verbose', '-s', 'libgazebo_ros_factory.so',world ],
            output='screen'),

        ExecuteProcess(
            cmd=['ros2', 'param', 'set', '/gazebo', 'use_sim_time', use_sim_time],
            output='screen'),

        ExecuteProcess(
            cmd=['ros2', 'run', 'ebot_gazebo', 'spawn_model.py'],
            output='screen'),

        # ExecuteProcess(
        #     cmd=['ros2', 'service', 'call', '/spawn_entity', 'gazebo_msgs/SpawnEntity', swpan_args],
        #     output='screen'),

         IncludeLaunchDescription(
            PythonLaunchDescriptionSource([launch_file_dir, '/robot_state_publisher.launch.py']),
            launch_arguments={'use_sim_time': use_sim_time}.items(),
        ),
        
    ])

