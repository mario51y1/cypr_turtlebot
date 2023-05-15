#!/usr/bin/env python3

import sys
import rospy
import cv2
import time
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Image
from std_msgs.msg import Int32
from cv_bridge import CvBridge

estado = 0
pub_mov = rospy.Publisher("/mobile_base/commands/velocity",Twist,queue_size = 10)

def movimiento():
    global pub_mov
    mov = Twist()
    v = 0.5
    if estado == 1:
        mov.linear.x = v
        mov.angular.z = 0.0
    elif estado == 2:
        mov.linear.x = -v
        mov.angular.z = 0.0
    elif estado == 3:
        mov.linear.x = 0.0
        mov.angular.z = v*2
    elif estado == 4:
        mov.linear.x = 0.0
        mov.angular.z = -v*2
    else:
        mov.linear.x = 0.0
        mov.angular.z = 0.0
    pub_mov.publish(mov)
        
        
def callback_matlab(dato):
    global estado, pub_mov
    mov = Twist()
    estado = dato.data
    print(dato.data)
    if estado >= 1 and estado <=4:
        movimiento()
    else:
        mov.linear.x = 0.0
        mov.angular.z = 0.0

def callback_image(image_raw):
    global estado
    bridge = CvBridge()
    try:
        print(estado)
        if estado == 40:
            print("dentro")
            image = bridge.imgmsg_to_cv2(image_raw,"passthrough")
            image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
            cv2.imwrite("src/turtlebot_mioelectrico/capturas/captura"+time.asctime()+".png",image)
            estado = 5 # por ejemplo 5
    except:
        rospy.logerr("CV_Bridge error")
            
def main(args):
    rospy.init_node('Base', anonymous=True) 
    rospy.Subscriber("/camera/rgb/image_raw",Image,callback_image)
    rospy.Subscriber("/sensor_matlab",Int32,callback_matlab)
        
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")

if __name__ == '__main__':
    main(sys.argv)
