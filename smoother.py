#!/usr/bin/env python

import rospy
import math
from std_msgs.msg import Float32

current = 0.0
target = 0.0

def callback(data):
    global target
    target = float("{0:.2f}".format(data.data))

def smoother():
    global current, target
    rospy.init_node("smoother", anonymous=True)
    rospy.Subscriber("command", Float32, callback)
    rate = rospy.Rate(10)
    while not rospy.is_shutdown(): 
        current = float("{0:.2f}".format(current))
        if target > current:
            current += 0.01
        elif target < current:
            current += -0.01
        print current
        rate.sleep()

if __name__ == '__main__':
    smoother()
