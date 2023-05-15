#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from chill_topic.msg import Chill_topic
import time
global tiempo
global contador
contador = 0
tiempo = 0.0 
def publicante():
    print('Ejecutando..')
    pub = rospy.Publisher('chill_topic',Chill_topic,queue_size=10)
    rospy.init_node('nodo_test',anonymous=True)
    rate = rospy.Rate(10)
    rospy.loginfo('Publicando')
    while not rospy.is_shutdown():
        global contador
        global tiempo
        if contador == 0:
            chill_data=Chill_topic()
            chill_data.signal1 = True
            chill_data.signal2 = False 
            chill_data.signal3 = False
            chill_data.signal4 = False
            chill_data.dist = 32.45
            chill_data.compass = 47.7
            chill_data.state = 2
            pub.publish(chill_data)
        

        contador = contador +1
        start = time.time()

        if contador >= 1:
            if tiempo <= 1.0:
                chill_data=Chill_topic()
                chill_data.signal1 = True
                chill_data.signal2 = False 
                chill_data.signal3 = False
                chill_data.signal4 = False
                chill_data.dist = 32.45
                chill_data.compass = 47.7
                chill_data.state = 2
                pub.publish(chill_data)

            if tiempo > 1.0:
                chill_data=Chill_topic()
                chill_data.signal1 = False
                chill_data.signal2 = True 
                chill_data.signal3 = False
                chill_data.signal4 = False
                chill_data.dist = 20.1
                chill_data.compass = 0.1
                chill_data.state = 3
                pub.publish(chill_data)
            
        end = time.time()
        tiempo_operando = float(end-start)
        tiempo = (tiempo_operando + tiempo)+0.080
        if tiempo > 2.0:
            tiempo = 0.0
        print(tiempo)


        
        
        rate.sleep()

if __name__ == '__main__':
    try:
        publicante()

    except rospy.ROSInterruptException:
        print('error')
        pass


