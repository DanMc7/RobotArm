from setuptools import find_packages, setup

package_name = 'tester_py'

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
    maintainer='danmc7',
    maintainer_email='danmc7@todo.todo',
    description='TODO: Package description',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
        	'publisher1 = tester_py.PublisherTester:main',
        	'subscriber1 = tester_py.SubscriberTester:main',
            'input1 = tester_py.InputTester:main',
            'motor_commands = tester_py.MotorInput:main',
            'motor_driver = tester_py.MotorDriver:main',
        ],
    },
)
