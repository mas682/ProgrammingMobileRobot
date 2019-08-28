#!/usr/bin/env python

import rospy
import math
from geometry_msgs.msg import Twist
from std_msgs.msg import Int8

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
    targetCommand.linear.x = float("{0:.2f}".format(data.data))
    targetCommand.angular.z = float("{0:.2f}".format(data.data))

def updateBrake(data):
    global brake
    brake = data

def cleanUp():
    global currentCommand
    currentCommand.linear.x = 0.0
    currentCommand.angular.z = 0.0
    pub.publish(currentCommand)
    rospy.sleep(1)

def velSmoother():
    global pub, targetCommand, currentCommand
    rospy.init_node("velocitySmoother", anonymous=True)
    rospy.Subscriber("kobuki_command", Twist, updateCommand)
    rospy.Subscriber("kobuki_brake", Int8, updateBrake)
    rospy.on_shutdown(cleanUp)

    while pub.get_num_connections() == 0:
        pass

    while not rospy.is_shutdown():
        if brake == 0
            if targetCommand.linear.x > currentCommand.linear.x:
                currentCommand.linear.x += 0.01
            elif targetCommand.linear.x < currentCommand.linear.x:
                currentCommand.linear.x += -0.01
            if targetCommand.angular.z > currentCommand.angular.z:
                currentCommand.angular.z += 0.01
            elif targetCommand.angular.z < currentCommand.angular.z:
                currentCommand.angular.z += -0.01
        elif brake == 1
            if targetCommand.linear.x > 0.0
                currentCommand.linear.x += -0.02
                if currentCommand.linear.x < 0
                    currentCommand.linear.x += 0.0
        elif brake == 2
            currentCommand.linear.x = 0
            currentCommand.angular.z = 0
        pub.publish(currentCommand)
        rospy.sleep(0.1)


if __name__ == '__main__':
    velSmoother()
