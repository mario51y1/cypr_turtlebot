#!/usr/bin/env python

import tkinter as tk
from tkinter import ttk
import cv2
from turtle import color
import tkinter.font as tkFont
import numpy as np
from PIL import ImageTk, Image
from tkinter import Tk, Label
import rospy
import rospkg
from std_msgs.msg import String
from chill_topic.msg import Chill_topic
global dist
global compass
global signal1
global signal2
global signal3
global signal4
global state

state = 0
dist = 0.0
compass = 0.0
signal1 = False
signal2 = False
signal3 = False
signal4 = False
def callback(data):
    global signal1, signal2, signal3, dist, compass, state, signal4
    signal1=data.signal1
    signal2=data.signal2
    signal3=data.signal3
    signal4=data.signal4
    dist = data.dist
    compass = data.compass
    state = data.state
    return signal1,signal2,signal3



def listener():
    rospy.init_node('listener',anonymous=True)
    rospy.Subscriber('chill_topic',Chill_topic,callback)

#------ interfaz ------
    wdow = tk.Tk()
    wdow.title("Chilling-out bot (explorer bot) status ")
    wdow.config(width=800,height=800)
    wdow.config(bg='gray16')
    status_display = tk.StringVar(value = 'Reposo')

    rospack = rospkg.RosPack()
    print(rospack.get_path('chill_topic'))
#    logo_raw = cv2.imread('/home/juancangaritan/Documents/MasterAR/Controlyprog/logo_hmi_corregido.png',cv2.IMREAD_UNCHANGED)

    logo_raw = cv2.imread(rospack.get_path('chill_topic') + '/resources/logo_hmi_corregido.png',cv2.IMREAD_UNCHANGED)
    ancho, alto, canales = logo_raw.shape
    ancho = int(ancho/1.8)
    alto = int(alto/1.8)

    img = cv2.resize(logo_raw,(ancho,alto),interpolation=cv2.INTER_AREA)
    img = Image.fromarray(img)
    img = ImageTk.PhotoImage(img)

    widthi, heighti = img.width(), img.height()
    print(widthi, heighti)
    canvas = tk.Canvas(wdow, bg= 'grey16', width=widthi, height=heighti, highlightthickness=0)
    canvas.place(x=5, y=5)
    canvas.create_image(0,0, image = img, anchor = 'nw')

    #---- Variable tk.variable
    global dist
    print_dist = round(dist,1)
    print_dist = str(print_dist)
    alturaVar = tk.StringVar(value='0.0')
    alturaVar.set(print_dist)

    global compass
    print_compass = round(compass,1)
    print_compass = str(print_compass)
    dirVar = tk.StringVar(value='0.0')
    dirVar.set(print_compass)

    signalVar = tk.StringVar(value='S1 = OFF')
    signalVar2 = tk.StringVar(value='S2 = OFF')
    signalVar3 = tk.StringVar(value='S3 = OFF')
    signalVar4 = tk.StringVar(value='Stime = OFF')
    # -------------- Bloque display altura -------------------
    fontConf = tkFont.Font(family='Arial',size=22,weight='bold', slant='italic')
    LabelAltura = Label(wdow, text = 'Distancia [m]',bg='grey16', fg ="grey60",font=fontConf).place(x=365, y= 50)

    fontDigital = tkFont.Font(family='times',size=10, weight='bold')

    altura_frame = tk.Frame(wdow,bg='black',width=150,height=50)
    altura_frame.place(x=620,y=50)
    altura_text = tk.Label(altura_frame,bg='black', textvariable=alturaVar,fg='red',font=('courier',30,'bold'))

    altura_text.pack(side='bottom', anchor='se')
    altura_frame.pack_propagate(False)

    fontConf = tkFont.Font(family='Arial',size=22,weight='bold', slant='italic')

#    ------- Bloque display Orientación ------
    LabelDir = Label(wdow, text = 'Dirección [deg°]',bg = 'grey16', fg='grey60',font=fontConf).place(x=365, y=150)
    dir_frame = tk.Frame(wdow,bg='black',width=150,height=50)
    dir_frame.place(x=620, y=150)
    dir_text = tk.Label(dir_frame,bg='black', textvariable=dirVar,fg='red',font=('courier',30,'bold'))
    dir_text.pack(side='bottom', anchor='se')
    dir_frame.pack_propagate(False)



    #------- Bloque señal 1 -----------

    signal_frame= tk.Frame(wdow, bg='firebrick',width = 100,height=50)
    signal_frame.place(x=365,y=250)
    signal_text=tk.Label(signal_frame,bg='firebrick',textvariable=signalVar,fg='black',font=('Arial',15,'bold'))
    signal_text.pack(side='bottom',anchor='sw')
    signal_frame.pack_propagate(False)


    #------- Bloque señal 2 -----------

    signal_frame2= tk.Frame(wdow, bg='firebrick',width = 100,height=50)
    signal_frame2.place(x=365+100+50,y=250)
    signal_text2=tk.Label(signal_frame2,bg='firebrick',textvariable=signalVar2,fg='black',font=('Arial',15,'bold'))
    signal_text2.pack(side='bottom',anchor='sw')
    signal_frame2.pack_propagate(False)


    #------- Bloque señal 2 -----------

    signal_frame3= tk.Frame(wdow, bg='firebrick',width = 100,height=50)
    signal_frame3.place(x=365+100+50+100+50,y=250)
    signal_text3=tk.Label(signal_frame3,bg='firebrick',textvariable=signalVar3,fg='black',font=('Arial',15,'bold'))
    signal_text3.pack(side='bottom',anchor='sw')
    signal_frame3.pack_propagate(False)


    #------- Bloque señal 2 -----------

    signal_frame4= tk.Frame(wdow, bg='firebrick',width = 150,height=50)
    signal_frame4.place(x=365+100+25,y=350)
    signal_text4=tk.Label(signal_frame4,bg='firebrick',textvariable=signalVar4,fg='black',font=('Arial',15,'bold'))
    signal_text4.pack(side='bottom',anchor='sw')
    signal_frame4.pack_propagate(False)


    #---- Label estado de maquina
    LabelEstadoMaquina = Label(wdow, text = 'Estado de máquina',bg='grey16', fg ="grey60",font=fontConf).place(x=35, y= 270+200)
    machinestatus_frame = tk.Frame(wdow,bg='black',width=550,height=50)
    machinestatus_frame.place(x=35,y=320+200)
    machinestatus_text = Label(machinestatus_frame,bg='black', text='Reposo',fg='lawn green',font=('courier',25))
    machinestatus_text.pack(side='bottom', anchor='sw')
    machinestatus_frame.pack_propagate(False)
    def update():
        global dist
        global compass
        global signal1
        global signal2
        global signal3
        global signal4
        global state
        #--- Variables Float ------
        dist= round(dist, 1)
        alturaVar.set(str(dist))
        
        compass = round(compass,1)
        dirVar.set(str(compass))

        #---- Sennales ----
        if signal1 == False:
            signal_frame.configure(bg='firebrick')
            signal_text.configure(bg='firebrick')
            signalVar.set('S1 = OFF')

        else:
            signal_frame.configure(bg='gold')
            signal_text.configure(bg='gold')
            signalVar.set('S1 = ON')


        #-- Sennal 2 --


        if signal2 == False:
            signal_frame2.configure(bg='firebrick')
            signal_text2.configure(bg='firebrick')
            signalVar2.set('S2 = OFF')

        else:
            signal_frame2.configure(bg='gold')
            signal_text2.configure(bg='gold')
            signalVar2.set('S2 = ON')
        #-- Sennal 3 --
        if signal3 == False:
            signal_frame3.configure(bg='firebrick')
            signal_text3.configure(bg='firebrick')
            signalVar3.set('S3 = OFF')

        else:
            signal_frame3.configure(bg='gold')
            signal_text3.configure(bg='gold')
            signalVar3.set('S3 = ON')
         #-- Sennal 4 --
        if signal3 == False:
            signal_frame4.configure(bg='firebrick')
            signal_text4.configure(bg='firebrick')
            signalVar4.set('Stime = OFF')

        else:
            signal_frame4.configure(bg='gold')
            signal_text4.configure(bg='gold')
            signalVar4.set('Stime = ON')

        if state == 1:
            machinestatus_text.configure(text='Reposo')
        elif state == 2:
            machinestatus_text.configure(text='Teleoperación')
        elif state == 3:
            machinestatus_text.configure(text='Captura de imagen')
        elif state == 4:
            machinestatus_text.configure(text='Mapeo automático')

        altura_text.after(100,update)
    update()
    wdow.mainloop()

if __name__=='__main__':
    listener()
