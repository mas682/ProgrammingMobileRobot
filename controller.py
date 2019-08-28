#!/usr/bin/env python

import rospy
from std_msgs.msg import Float32

def controller():
    pub = rospy.Publisher("command", Float32, queue_size = 10)
    rospy.init_node("controller", anonymous=True)
    while not rospy.is_shutdown():
        number = input("Please enter a floating-point number:")
        number = float(number)
        pub.publish(number)    

if __name__== '__main__':
    try:
        controller()
    except rospy.ROSInterruptException:
        pass


