#!/usr/bin/env python

import rospy
from std_msgs.msg import ByteMultiArray
from std_msgs.msg import String
import tty, sys, termios

pub = rospy.Publisher("keyboard_control",ByteMultiArray, queue_size = 10)
keys = [0, 0, 0, 0, 0, 0, 0]
byte_array = ByteMultiArray()


def checkKey(key_value):
    global pub
    button_pushed = 0   # variable used so that array not published if invalid input hit
    if key_value == 106:  # j...turn left
        button_pushed = 1
        keys[0] = 1
    else:
        keys[0] = 0
    if key_value == 105: # i...move straight
        button_pushed = 1
        keys[1] = 1
    else:
        keys[1] = 0
    if key_value == 108: # l...move right
        button_pushed = 1
        keys[2] = 1
    else:
        keys[2] = 0
    if key_value == 32: # space...main brake
        button_pushed = 1
        keys[3] = 1
    else:
        keys[3] = 0
    if key_value == 98: # b...move backwards
        button_pushed = 1
        keys[4] = 1
    else:
        keys[4] = 0
    if key_value == 9: # tab...emergency break
        button_pushed = 1
        keys[5] = 1
    else:
        keys[5] = 0
    if key_value == 113: # q...stop robot as keyboard disconnected
        button_pushed = 1
        keys[6] = 1
    else:
        keys[6] = 0
    global pub
    if button_pushed == 1:
        byte_array.data = keys      # .data is where the array is held in the byte array
        pub.publish(byte_array)


def cleanUp():
    global pub
    keys = [0, 0, 0, 0, 0, 0, 0]
    byte_array.data = keys
    pub.publish(byte_array)
    rospy.sleep(1)

def keyboard():
    global pub
    rospy.init_node("keyboardControl", anonymous = True)
    rospy.on_shutdown(cleanUp)
    while pub.get_num_connections() == 0:
        pass
    print "Press q to terminate the program"
    ch = ""
    while not ch == "q":
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        sys.stdout.write
        print ord(ch)
        checkKey(ord(ch))

if __name__=='__main__':
    keyboard()
