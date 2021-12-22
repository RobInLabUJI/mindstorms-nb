import json
import shutil

from IPython.core.display import display, HTML

def configure(n):
    config = {
        'version' : 'ev3',
        'number' : n
    }
    with open('../task/robot_config.json', 'w') as f:
        json.dump(config, f)
    shutil.copyfile('./functions.py', '../task/functions.py')
    print("\x1b[32mConfiguració completa.\x1b[0m")

    display(HTML('<p>Ara ja podeu continuar, començant la primera tasca de programació: provareu el robot a vore si respon i es mou correctament.</p><h2><a href="../task/index.ipynb" target="_blank">&gt;&gt;&gt; Prova de connexió</a></h2>'))

def next_notebook(nb):
    if nb=='moviments':
        display(HTML('<p>Ja podeu passar a la pàgina següent, on aprendreu a controlar els moviments del robot:</p><h2><a href="motors.ipynb" target="_blank">&gt;&gt;&gt; Moviments del robot</a></h2>'))
    elif nb=='quadrat':
        display(HTML('<p>Ara ja podeu continuar, bona sort!</p><h2><a href="quadrat.ipynb" target="_blank">&gt;&gt;&gt; Exercici de moviment</a></h2>'))
    elif nb=='sensors':
        display(HTML('<p>Fins ara heu aprés a controlar el moviment del robot, i també a programar bucles, no està gens malament!</p><p>Per a continuar, anem a vore els altres components del robot, els sensors, que ens permetran fer programes encara més sofisticats.</p><h2><a href="sensors.ipynb" target="_blank">&gt;&gt;&gt; Sensors</a></h2>'))
    elif nb=='touch':
        display(HTML('<p>Ara ja podeu passar al primer exercici amb sensors:</p><h2><a href="touch.ipynb" target="_blank">&gt;&gt;&gt; Tacte</a></h2>'))
    elif nb=='navigation':
        display(HTML('<p>Ara ja podeu continuar.</p><h2><a href="navigation.ipynb" target="_blank">&gt;&gt;&gt; Exercici de navegació</a></h2>'))
    elif nb=='sound':
        display(HTML('<p>Ara ja podeu continuar.</p><h2><a href="sound.ipynb" target="_blank">&gt;&gt;&gt; Sensor de so</a></h2>'))
    elif nb=='light':
        display(HTML('<p>Ara ja podeu continuar.</p><h2><a href="light.ipynb" target="_blank">&gt;&gt;&gt; Sensor de llum</a></h2>'))
    elif nb=='ultrasonic':
        display(HTML('<p>Ara ja podeu continuar.</p><h2><a href="ultrasonic.ipynb" target="_blank">&gt;&gt;&gt; Sensor ultrasònic</a></h2>'))
    elif nb=='sumo':
        display(HTML('<p>Ara ja podeu continuar.</p><h2><a href="sumo.ipynb" target="_blank">&gt;&gt;&gt; El Gran Repte</a></h2>'))
    else:
        pass

import ev3_dc as ev3

def connect():
    global brick
    global address
    global mB; global mC
    global ts; global gy; global us; global cl; global so
    global snd
    global tempo
    global connected_robot
    with open('robot_config.json', 'r') as f:
         config = json.load(f)
    n = config['number']
    try:
        address = {1: '00:16:53:51:07:8F',\
		   2: '00:16:53:53:F1:8D',\
		   3: '',\
		   4: '00:16:53:51:5F:3C',\
		   5: '00:16:53:53:83:0C'}
        brick = ev3.EV3(protocol=ev3.BLUETOOTH, host=address[n])
        mB = ev3.Motor(ev3.PORT_B, ev3_obj=brick)
        mC = ev3.Motor(ev3.PORT_C, ev3_obj=brick)
        ts = ev3.Touch(ev3.PORT_1, ev3_obj=brick)
        #so = ev3.SoundSensor('in2')
        #so.mode='DB'
        us = ev3.Ultrasonic(ev3.PORT_4, ev3_obj=brick)
        cl = ev3.Color(ev3.PORT_3, ev3_obj=brick)
        snd = ev3.Sound(ev3_obj=brick)
        tempo = 0.25
        connected_robot = n
        print("\x1b[32mRobot %d connectat.\x1b[0m" % n)
    except KeyError:
        print("\x1b[31mNúmero de robot incorrecte.\x1b[0m")
    except ev3.exceptions.NoEV3:
        print("\x1b[31mNo es pot connectar amb el robot.\x1b[0m")
    except OSError:
        print("\x1b[33mError de connexió. Intenta-ho de nou, si segueix sense funcionar avisa el professor.\x1b[0m")

def disconnect():
    try:
        brick.__del__()
        print("\x1b[32mRobot %d desconnectat.\x1b[0m" % connected_robot)
    except NameError:
        print("\x1b[31mNo hi ha connexió amb el robot.\x1b[0m")

def stop():
    try:
        mB.stop()
        mC.stop()
    except (NameError, EOFError, OSError):
        print("\x1b[31mNo hi ha connexió amb el robot.\x1b[0m")

def forward(speed=100,speed_B=100,speed_C=100):
    move(speed_B=min(abs(speed),abs(speed_B)),speed_C=min(abs(speed),abs(speed_C)))
    
def backward(speed=100,speed_B=100,speed_C=100):
    move(speed_B=-min(abs(speed),abs(speed_B)),speed_C=-min(abs(speed),abs(speed_C)))
    
def left(speed=100):
    move(speed_B=0,speed_C=abs(speed))

def right(speed=100):
    move(speed_B=abs(speed),speed_C=0)
    
def left_sharp(speed=100):
    move(speed_B=-abs(speed),speed_C=abs(speed))
       
def right_sharp(speed=100):
    move(speed_B=abs(speed),speed_C=-abs(speed))

import math

def move(speed_B=0,speed_C=0):
    max_speed = 100
    direction_B = int(math.copysign(1, speed_B))
    speed_B = int(abs(speed_B))
    direction_C = int(math.copysign(1, speed_C))
    speed_C = int(abs(speed_C))
    if speed_B > 100:
        speed_B = 100
        print("\x1b[33mLa velocitat màxima és 100.\x1b[0m")
    if speed_C > 100:
        speed_C = 100
        print("\x1b[33mLa velocitat màxima és 100.\x1b[0m")
    try:
        speed_B = int(speed_B*max_speed/100)
        speed_C = int(speed_C*max_speed/100)
        if speed_B > 0:
            mB.speed=speed_B
        if speed_C > 0:
            mC.speed=speed_C
        if speed_B > 0:
            mB.start_move(direction=direction_B)
        if speed_C > 0:
            mC.start_move(direction=direction_C)
    except (NameError, EOFError, OSError):
        print("\x1b[31mNo hi ha connexió amb el robot.\x1b[0m")
    
def touch():
    return ts.touched

#def gyro():
#    return gy.value()

def sound():
    return 0

def ultrasonic():
    try:
        return us.distance / 10
    except TypeError:
        return 2.55

def light():
    return cl.reflected

#def beep():
#    snd.beep()
    
def play_tone(f,t):
    snd.tone(f,int(t*tempo))
    
#def speak(s):
#    snd.speak(s).wait()
    
from IPython.display import clear_output

def read_and_print(sensor):
    try:
        while True:
            clear_output(wait=True)
            print(sensor())
    except KeyboardInterrupt:
        pass
    
def test_sensors():
    try:
        while True:
            clear_output(wait=True)
            print("     Touch: %d\n     Light: %d\n     Sound: %d\nUltrasonic: %.2f" % (touch(),light(),sound(), ultrasonic()))
    except KeyboardInterrupt:
        pass
    
import matplotlib.pyplot as plt

def plot(l):
    plt.plot(l)
