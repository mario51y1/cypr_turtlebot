import rospy
import smach
import cv2
import time

from geometry_msgs.msg import Twist
from sensor_msgs.msg import Image
from std_msgs.msg import Int32
from cv_bridge import CvBridge


estado = 0
pub_mov = rospy.Publisher("/mobile_base/commands/velocity",Twist,queue_size = 10)
current_image = None
sm = None



class Standby(smach.State):
    def __init__(self) -> None:
        smach.State.__init__(self, outcomes=['Standby','Camara', 'Mapa', 'MovLinear'],input_keys=['input'],output_keys=['input'])
               
        
    def execute(self, userdata):
        time.sleep(0.5)
        return_value = None
        if userdata.input == 0 or userdata.input==4:
            return_value = 'Standby'
        elif userdata.input == 1:
            return_value = 'MovLinear'
        elif userdata.input == 2:
            return_value = 'Mapa'
        elif userdata.input == 3:
            return_value = 'Camara'
        userdata.input = 0
        return return_value

     
class MovLinear(smach.State):
    def __init__(self) -> None:
        smach.State.__init__(self, outcomes=['MovLinear','Standby', 'MovAngular'],input_keys=['input'],output_keys=['input'])

    def execute(self, userdata):
        time.sleep(0.5)
        global pub_mov
        mov = Twist()
        mov.linear.x = 0
        mov.angular.z = 0
        v = 0.5
        return_value = None
        if userdata.input == 0:
            return_value = 'MovLinear'
        elif userdata.input == 1:
            mov.linear.x = v
            print('Linear v')
            return_value = 'MovLinear'
        elif userdata.input == 2:
            mov.linear.x = -v
            print('Linear -v')
            return_value = 'MovLinear'
        elif userdata.input == 3:
            return_value = 'MovAngular'
        elif userdata.input == 4:
            return_value = 'Standby'
        pub_mov.publish(mov)
        userdata.input = 0
        return return_value

class MovAngular(smach.State):
    def __init__(self) -> None:
        smach.State.__init__(self, outcomes=['MovAngular','Standby', 'MovLinear'],input_keys=['input'],output_keys=['input'])
    def execute(self, userdata):
        time.sleep(0.5)
        global pub_mov
        mov = Twist()
        mov.linear.x = 0
        mov.angular.z = 0
        v = 0.5
        return_value = None
        if userdata.input == 0:
            return_value = 'MovAngular'
        elif userdata.input == 1:
            mov.angular.z = v*2
            print('Angular v')
            return_value = 'MovAngular'
        elif userdata.input == 2:
            mov.angular.z = -v*2
            print('Angular -v')
            return_value = 'MovAngular'
        elif userdata.input == 3:
            return_value = 'MovLinear'
        elif userdata.input == 4:
            return_value = 'Standby'
        pub_mov.publish(mov)
        userdata.input = 0
        return return_value

class Camara(smach.State):
    def __init__(self) -> None:
        smach.State.__init__(self, outcomes=['Camara','Standby'],input_keys=['input'],output_keys=['input'])
    def execute(self, userdata):
        time.sleep(0.5)
        return_value = None
        if userdata.input == 0 or userdata.input == 2 or userdata.input == 4:
            return_value = 'Camara'
        elif userdata.input == 1:
            #Cosa de hacer foto
            cv2.imwrite("src/turtlebot_mioelectrico/capturas/captura"+time.asctime()+".png",current_image)
            print('Hago foto')
            return_value = 'Camara'
        elif userdata.input == 3:
            return_value = 'Standby'
        userdata.input = 0
        return return_value

class Mapa(smach.State):
    def __init__(self) -> None:
        smach.State.__init__(self, outcomes=['Mapa','Standby'],input_keys=['input'],output_keys=['input'])
    def execute(self, userdata):
        time.sleep(0.5)
        return_value = None
        if userdata.input == 0 or userdata.input == 4:
            return_value = 'Mapa'
        elif userdata.input == 1:
            #Cosa mapa ON
            print('Mapa on')
            return_value = 'Mapa'
        elif userdata.input == 2:
            #Cosa de mapa OFF
            print('Mapa off')
            return_value = 'Mapa'
        elif userdata.input == 3:
            return_value = 'Standby'
        userdata.input = 0
        return return_value

def get_state_machine():
    sm = smach.StateMachine(outcomes=['outcome4', 'outcome5'])
    sm.userdata.input = 0
    with sm:
        smach.StateMachine.add('Standby', Standby(),
                               transitions={
                                   'Standby': 'Standby',
                                   'Camara': 'Camara',
                                   'Mapa': 'Mapa',
                                   'MovLinear': 'MovLinear'
                                   },
                               remapping={'input': 'input'}
                               )
        smach.StateMachine.add('MovLinear', MovLinear(),
                               transitions={
                                    'MovLinear': 'MovLinear',
                                    'Standby': 'Standby',
                                    'MovAngular': 'MovAngular'
                                    },
                               remapping={'input': 'input'}
                               )
        smach.StateMachine.add('MovAngular', MovAngular(),
                               transitions={
                                    'MovAngular': 'MovAngular',
                                    'Standby': 'Standby',
                                    'MovLinear': 'MovLinear'
                                    },
                               remapping={'input': 'input'}
                               )
        smach.StateMachine.add('Mapa', Mapa(),
                               transitions={
                                    'Mapa': 'Mapa',
                                    'Standby': 'Standby'
                                    },
                               remapping={'input': 'input'}
                               )
        smach.StateMachine.add('Camara', Camara(),
                               transitions={
                                    'Camara': 'Camara',
                                    'Standby': 'Standby',
                                    },
                               remapping={'input': 'input'}
                               )

    return sm

def callback_matlab(dato):
    sm.userdata.input = dato.data
    print(sm.userdata.input)
    
def callback_image(image_raw):
    global estado
    bridge = CvBridge()
    try:
        current_image = bridge.imgmsg_to_cv2(image_raw,"passthrough")
        current_image = cv2.cvtColor(current_image,cv2.COLOR_BGR2RGB)
        cv2.imshow(current_image)
    except:
        rospy.logerr("CV_Bridge error")
 
def main():
    global sm 
    rospy.init_node('controlessss') 
    rospy.Subscriber("/camera/rgb/image_raw",Image,callback_image)
    rospy.Subscriber("/sensor_matlab",Int32,callback_matlab)

    sm = get_state_machine()
    sm.execute()
    
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print('Shutdown')

if __name__=='__main__':
    main()
