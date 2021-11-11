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
    #lines = []  
    #print(lines)
    #print(lines[0].strip()[-3:])

    if lines == []:
        print("ERROR")
        return setpoint
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

GPIO.setup(32,GPIO.OUT) #heater pin 
p = GPIO.PWM(32,60)
p.start(0)

#GPIO.setup(37,GPIO.OUT) #humidif. pin 

setpoint = 38  #em graus celsius
kP = 60
kI = 0.1
kD = 0.5
potMax=90

p.ChangeDutyCycle(0)

def main():
    #print("PWM Gerado!")
    global lastTemp
    global tempRead
    global I

    delay.sleep(0.1)
    lastTemp=tempRead
    tempRead=read_temp()

    #PID Cicle
    error = setpoint - tempRead
    P = error*kP
    I += error*kI
    if (I >= potMax-50): #quando esta esquentando (inicialmente frio) nao acumular muito I
        I=potMax-50
    D = (lastTemp-tempRead)*kD
    PID = P + I + D
    print("P:",round(P,2)," I:",round(I,2)," D:",round(D,2))
    #print(round(PID,2))
    if (PID >= potMax-50):  #limitar potencia max
        PID = potMax-50
    elif (PID <= -50):  #limitar potencia minima
        PID = -50
    p.ChangeDutyCycle(PID+50) #p.ChangeDutyCycle(PID+X) x=50 
    #print("PID: ",round(PID,2),"I: ",round(I,2))
    print("Temp: ",round(tempRead,2),"C  Erro: ", round(error,2),"C  Potencia: ",round(PID+50,2),"%") 
        
        
if __name__ == "__main__":
    global lastTemp
    global tempRead
    global I
    lastTemp=0
    tempRead=0
    I = 0

    while(1):
        main()
    
