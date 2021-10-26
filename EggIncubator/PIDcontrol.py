import RPi.GPIO as GPIO
import time as delay

import os
import glob
import time

#ds18b20
 
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
 
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'
 
def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines
 
def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c

#pwm

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(32,GPIO.OUT)

p = GPIO.PWM(32,10)
p.start(0)

tempRead=0
setpoint = 38
kP = 30
kI = 1
kD = 1
PID = 0
P = 0
I = 0
D = 0

p.ChangeDutyCycle(70)

try:
    print("PWM Gerado!")
    while(1):
        delay.sleep(0.1)
        lastTemp=tempRead
        tempRead=read_temp()

        #PID Cicle
        error = setpoint - tempRead
        P = error*kP
        I += error*kI
        D = (lastTemp-tempRead)*kD
        PID = P + I + D
        if (PID >= 50):
            PID = 50
            p.ChangeDutyCycle(70)
            print("1 ",tempRead, error, PID)
        elif (PID <= -50):
            PID= -50
            p.ChangeDutyCycle(0)
            print("2 ",tempRead, error, PID)            
        elif (PID < 50 and PID > 0):
            p.ChangeDutyCycle(PID+50)
            print("3 ",tempRead, error, PID)
        elif (PID < 0):
            p.ChangeDutyCycle(PID+50)
            print("4 ",tempRead, error, PID)
        
        
            
except KeyboardInterrupt:
    pass
p.stop()
GPIO.cleanup()
