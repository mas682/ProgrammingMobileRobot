#!/usr/bin/env python

import rospy
import math
from geometry_msgs.msg import Twist
from std_msgs.msg import Int32

pub = rospy.Publisher("/mobile_base/commands/velocity", Twist, queue_size=10)
currentCommand = Twist()
currentCommand.linear.x = 0.0
currentCommand.angular.z = 0.0
targetCommand = Twist()
targetCommand.linear.x = 0.0
targetCommand.angular.z = 0.0
brake = 0

def updateCommand(data):
    global targetCommand
    targetCommand = data
    targetCommand.linear.x = float("{0:.2f}".format(targetCommand.linear.x))
    targetCommand.angular.z = float("{0:.2f}".format(targetCommand.angular.z))

def updateBrake(data):
    global brake
    brake = data.data

def cleanUp():
    global currentCommand
    currentCommand.linear.x = 0.0
    currentCommand.angular.z = 0.0
    pub.publish(currentCommand)
    rospy.sleep(1)

def velSmoother():
    global pub, targetCommand, currentCommand, brake
    rospy.init_node("velocitySmoother", anonymous=True)
    rospy.Subscriber("kobuki_command", Twist, updateCommand)
    rospy.Subscriber("kobuki_brake", Int32, updateBrake)
    rospy.on_shutdown(cleanUp)

    while pub.get_num_connections() == 0:
        pass

    while not rospy.is_shutdown():
        #Sometimes we will need different rates of acceleration, like when braking
        acceleration_x = 0.05
	acceleration_z = 0.5
	#Account for braking
        if brake == 1:
            targetCommand.linear.x = 0.0
            targetCommand.angular.z = 0.0
            acceleration_x = 2 * acceleration_x
            acceleration_z = 2 * acceleration_z
        elif brake == 2:
            targetCommand.linear.x = 0.0
            targetCommand.angular.z = 0.0
            currentCommand.linear.x = 0.0
            currentCommand.angular.z = 0.0
        #Accelerate towards target
        if targetCommand.linear.x > currentCommand.linear.x:
            currentCommand.linear.x += acceleration_x
        elif targetCommand.linear.x < currentCommand.linear.x:
            currentCommand.linear.x -= acceleration_x
        if targetCommand.angular.z > currentCommand.angular.z:
            currentCommand.angular.z += acceleration_z
        elif targetCommand.angular.z < currentCommand.angular.z:
            currentCommand.angular.z -= acceleration_z
        #To prevent stuttering
        if math.fabs(targetCommand.linear.x - currentCommand.linear.x) < acceleration_x:
            currentCommand.linear.x = targetCommand.linear.x
        if math.fabs(targetCommand.angular.z - currentCommand.angular.z) < acceleration_z:
            currentCommand.angular.z = targetCommand.angular.z
        #Publish and wait
        pub.publish(currentCommand)
        rospy.sleep(0.1)


if __name__ == '__main__':
    velSmoother()
