#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist
from std_msgs.msg import Int32, ByteMultiArray
import time

pub = rospy.Publisher("kobuki_command", Twist, queue_size=10)
brakePub = rospy.Publisher("kobuki_brake", Int32, queue_size=10)
buttons = [0, 0, 0, 0, 0, 0, 0]
command = Twist()
brake = 0
start = 0.0

# added this so that when the gas pedal is let go or right/left turn, then
# the robot will keep moving at speed for some period of time..2 seconds for now..
# and then it will slow down but not like braking
def getTime():
    global start
    end = time.time()
    return end - start

def keyboardCallback(data):
    global buttons, axes, start
    buttons = data.data
    start = time.time()


def cleanUp():
    global pub, command
    command.linear.x = 0.0
    command.angular.z = 0.0
    pub.publish(command)
    rospy.sleep(1)

def remoteController():
    global pub, command, buttons
    max_speed = 0.8
    rospy.init_node("remoteControl", anonymous=True)
    rospy.Subscriber("keyboard_control", ByteMultiArray, keyboardCallback)
    rospy.on_shutdown(cleanUp)
    current_speed = 0.0
    current_turn = 0.0

    while pub.get_num_connections() == 0:
        pass

    while not rospy.is_shutdown():
	brake = 0
        #forwards and backwards
        if buttons[1] == 1:
            command.linear.x = 0.8
        elif buttons[4] == 1:
                command.linear.x = -0.8
        else:
            command.linear.x = 0.0
        #left and right
        if buttons[0] == 1:
            command.angular.z = 1.0
        elif buttons[2] == 1:
            command.angular.z = -1.0
        else:
            command.angular.z = 0.0

        #break and emergency break
        if buttons[3]:
            brake = 1
        if buttons[5] or buttons[6]:  # if emergency break or keyboard hutting down
            brake = 2
        #TODO ludicrous speed?
        # set a timer so if no buttons pushed during time, go back to 0
        # timer reset any time a button is pushed
        if getTime() > 2.0:
            command.linear.x = 0.0
            command.angular.z = 0.0
        pub.publish(command)
        brakePub.publish(brake)

if __name__ == '__main__':
    remoteController()
