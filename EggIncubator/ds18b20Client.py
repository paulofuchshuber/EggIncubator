import RPi.GPIO as GPIO
import time

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
        return tempRead
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


tempRead=0
I = 0
totalTimer=0
sumAvarTemp=0
sumAvarPower=0
minTemp=read_temp()
maxTemp=minTemp
power=0

p.ChangeDutyCycle(power)

def main():
    global tempRead
    global I
    global totalTimer
    global sumAvarTemp
    global sumAvarPower
    global minTemp
    global maxTemp
    global power
    periodicidade = 60              #em segundos

    startTimer=time.time()

    time.sleep(0.1)
    lastTemp=tempRead
    lastPower=power
    tempRead=read_temp()

    #PID Cicle
    error = setpoint - tempRead
    P = error*kP
    I += error*kI
    if (I >= potMax-50):            #quando esta esquentando (inicialmente frio) nao acumular muito I
        I=potMax-50
    D = (lastTemp-tempRead)*kD
    PID = P + I + D
    #print("P:",round(P,2)," I:",round(I,2)," D:",round(D,2))
    if (PID >= potMax-50):          #limitar potencia max
        PID = potMax-50
    elif (PID <= -50):              #limitar potencia minima
        PID = -50
    power=PID+50
    p.ChangeDutyCycle(power)       #p.ChangeDutyCycle(PID+X) x=50 
    #print("PID: ",round(PID,2),"I: ",round(I,2))
    print("Temp: ",round(tempRead,2),"C  Erro: ", round(error,2),"C  Potencia: ",round(power,2),"%") 

    #data manipulation for upload
    if (tempRead<minTemp):
        minTemp=tempRead
    elif (tempRead>maxTemp):
        maxTemp=tempRead        

    elapsedTime=(time.time())-startTimer
    totalTimer+=elapsedTime
    sumAvarTemp+=tempRead*elapsedTime
    sumAvarPower+=lastPower*elapsedTime
    

    weigAvarTemp=sumAvarTemp/totalTimer         #essa parte pode passar pra dentro da prox condicional
    weigAvarPower=sumAvarPower/totalTimer       #essa tambem
    
    print("delay: ",round(elapsedTime,2)," Total tempo decorrido: ",round(totalTimer,2)," Med. Pond: ",round(weigAvarTemp,2), " Power: ",round(weigAvarPower,2))
    print("minTemp: ",round(minTemp,2)," maxTemp: ",round(maxTemp,2))
    print("")

    if (totalTimer >= periodicidade):
        print("")
        print("Total Tempo decorrido: ",round(totalTimer,2)," Med. Pond: ", round(weigAvarTemp,2))
        print("minTemp: ",round(minTemp,2)," maxTemp: ",round(maxTemp,2)," Media Pot: ",round(weigAvarPower,2))
        print("")
        totalTimer=0
        sumAvarTemp=0
        sumAvarPower=0
        maxTemp=tempRead
        minTemp=tempRead


    
        
        
if __name__ == "__main__":

    while(1):
        main()
    
