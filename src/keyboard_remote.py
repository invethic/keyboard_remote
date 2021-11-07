import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist

import sys
import tty
import termios
import asyncio



power_val = 50
key = 'status'
normalize_speed =100
print("If you want to quit.Please press q")
def readchar():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def readkey(getchar_fn=None):
    getchar = getchar_fn or readchar
    c1 = getchar()
    if ord(c1) != 0x1b:
        return c1
    c2 = getchar()
    if ord(c2) != 0x5b:
        return c1
    c3 = getchar()
    return chr(0x10 + ord(c3) - 65)

def Keyborad_control():
    pub = rospy.Publisher("cmd_vel",Twist,queue_size=10)
    rospy.init_node("Keyboard_publisher")

    vel_msg = Twist()

    while True:
        global power_val
        key=readkey()
        if key=='6':
            if power_val <=90:
                power_val += 10
                print("power_val:",power_val)
               
        elif key=='4':
            if power_val >=10:
                power_val -= 10
                print("power_val:",power_val)

        vel_msg.linear.x = power_val 
        if key=='w':
            vel_msg.angular.z = 0
        elif key=='a':
            # pass
            vel_msg.angular.z = 1
        elif key=='s':
            # pass
            vel_msg.angular.z = 0
            vel_msg.linear.x= -power_val
        elif key=='d':
            # pass
            vel_msg.angular.z = -1
        else:
            vel_msg.linear.x = 0
            # print("stopping")
        if key=='q':
            print("quit")  
            break  
        pub.publish(vel_msg)
if __name__ == '__main__':
    Keyborad_control()