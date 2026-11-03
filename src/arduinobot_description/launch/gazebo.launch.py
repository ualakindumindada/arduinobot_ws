from launch import LaunchDescription
from launch.actions import (
    SetEnvironmentVariable,
    IncludeLaunchDescription,
    DeclareLaunchArgument
)
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from ament_index_python.packages import get_package_share_directory

from pathlib import Path
import os


def generate_launch_description():

    # Get package directory
    pkg_share = get_package_share_directory("arduinobot_description")

    # Robot model path
    model_arg = DeclareLaunchArgument(
        name="model",
        default_value=os.path.join(
            pkg_share,
            "urdf",
            "arduinobot.urdf.xacro"
        ),
        description="Absolute path to robot URDF/Xacro file"
    )

    # Set Gazebo resource path
    gazebo_resource_path = SetEnvironmentVariable(
        name="GZ_SIM_RESOURCE_PATH",
        value=str(Path(pkg_share).parent.resolve())
    )

    # Process Xacro
    robot_description = ParameterValue(
        Command([
            "xacro ",
            LaunchConfiguration("model")
        ]),
        value_type=str
    )

    # Robot State Publisher
    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        output="screen",
        parameters=[
            {"robot_description": robot_description},
            {"use_sim_time": True}
        ]
    )

    # Launch Gazebo
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory("ros_gz_sim"),
                "launch",
                "gz_sim.launch.py"
            )
        ),
        launch_arguments={
            "gz_args": "-r -v 4 empty.sdf"
        }.items()
    )

    # Spawn robot in Gazebo
    gz_spawn_entity = Node(
        package="ros_gz_sim",
        executable="create",
        arguments=[
            "-name", "arduinobot",
            "-topic", "robot_description"
        ],
        output="screen"
    )

    # ROS-Gazebo bridge
    gz_ros2_bridge = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        arguments=[
            "/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock"
        ],
        output="screen"
    )

    return LaunchDescription([
        gazebo_resource_path,
        gazebo,
        model_arg,
        robot_state_publisher,
        gz_spawn_entity,
        gz_ros2_bridge
    ])
