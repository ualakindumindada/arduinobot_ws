from setuptools import find_packages, setup

package_name = 'arduinobot'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='lakindu',
    maintainer_email='lakindu@todo.todo',
    description='ArduinoBot ROS 2 Python package',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'simple_publisher = arduinobot.simple_publisher:main',
            'simple_subscriber = arduinobot.simple_subscriber:main',
        ],
    },
)