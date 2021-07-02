#!/usr/bin/env python3
import os
import sys
import rclpy
from ament_index_python.packages import get_package_share_directory
from gazebo_msgs.srv import SpawnEntity

def main():
    """ Main for spwaning turtlebot node """
    # Get input arguments from user
    

    # Start node
    rclpy.init()
    sdf_file_path = os.path.join(
        get_package_share_directory("ebot_gazebo"), "models",
        "ebot", "ebot_ur5_2.urdf")
    node = rclpy.create_node("entity_spawner")

    node.get_logger().info(
        'Creating Service client to connect to `/spawn_entity`')
    client = node.create_client(SpawnEntity, "/spawn_entity")

    node.get_logger().info("Connecting to `/spawn_entity` service...")
    if not client.service_is_ready():
        client.wait_for_service()
        node.get_logger().info("...connected!")

    # Get path to the turtlebot3 burgerbot
    # sdf_file_path = os.path.join(
    #     get_package_share_directory("turtlebot3_gazebo"), "models",
    #     "turtlebot3_burger", "model-1_4.sdf")

    # Set data for request
    request = SpawnEntity.Request()
    request.name = 'sahayak_bot'
    request.xml = open(sdf_file_path, 'r').read()
    request.robot_namespace = 'sahayak_bot'
    request.initial_pose.position.x = float(0.00)
    request.initial_pose.position.y = float(0.00)
    request.initial_pose.position.z = float(0.18)

    node.get_logger().info("Sending service request to `/spawn_entity`")
    future = client.call_async(request)
    rclpy.spin_until_future_complete(node, future)
    if future.result() is not None:
        print('response: %r' % future.result())
    else:
        raise RuntimeError(
            'exception while calling service: %r' % future.exception())

    node.get_logger().info("Done! Shutting down node.")
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()