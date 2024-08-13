from setuptools import setup

package_name = 'ros2_mqtt_converter'

setup(
    name=package_name,
    version='1.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Mike Likes Robots',
    maintainer_email='mikelikesrobots@outlook.com',
    description='AWS IoT connectivity samples for ROS2',
    license='MIT-0',
    entry_points={
        'console_scripts': [
            'converter = ros2_mqtt_converter.converter:main',
        ],
    },
)
