from setuptools import find_packages, setup

package_name = 'tf2_lessons'

setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Abhinav Giri',
    maintainer_email='24bsm001@iiitdmj.ac.in',
    description='SM3012 TF2 exercise solutions (all 9 exercises)',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'sensor_mounts    = tf2_lessons.sensor_mounts:main',
            'figure_eight     = tf2_lessons.figure_eight:main',
            'odometer         = tf2_lessons.odometer:main',
            'obstacle_mapper  = tf2_lessons.obstacle_mapper:main',
            'time_traveller   = tf2_lessons.time_traveller:main',
            'broken           = tf2_lessons.broken:main',
            'broken_original  = tf2_lessons.broken_original:main',
            'robot_a          = tf2_lessons.robot_a:main',
            'robot_b          = tf2_lessons.robot_b:main',
            'rendezvous       = tf2_lessons.rendezvous:main',
        ],
    },
)