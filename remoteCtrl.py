#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist
from std_msgs.msg import Int32

pub = rospy.Publisher("kobuki_command", Twist, queue_size=10)
brakePub = rospy.Publisher("kobuki_brake", Int32, queue_size=10)
buttons = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
axes = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
command = Twist()
brake = 0

def joystickCallback(data):
    global buttons, axes
    buttons = data.buttons
    axes = data.axes

def cleanUp():
    global pub, command
    command.linear.x = 0.0
    command.angular.z = 0.0
    pub.publish(command)
    rospy.sleep(1)

def remoteController():
    global pub, command, buttons, axes
    max_speed = 0.8
    rospy.init_node("remoteControl", anonymous=True)
    rospy.Subscriber("joy", Joy, joystickCallback)
    rospy.on_shutdown(cleanUp)
    
    while pub.get_num_connections() == 0:
        pass

    while not rospy.is_shutdown():
	brake = 0
        #forwards and backwards
	command.linear.x = max_speed * axes[1]
        #left and right
        command.angular.z = axes[0]
        #break and emergency break
        if buttons[0]:
            brake = 1
        if buttons[1]:
            brake = 2
        #TODO ludicrous speed?
        pub.publish(command)
        brakePub.publish(brake)

if __name__ == '__main__':
    remoteController()
