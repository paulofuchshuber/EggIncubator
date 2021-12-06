import RPi.GPIO as GPIO
import time
import datetime
import os
import glob
import time
import dynamoFunctions
from socketIO_client import SocketIO
import signal
import json

#SOCKET SETTINGS
def handler(signum, frame):
    print('Action took too much time')
    raise Exception('Action took too much time')
    

signal.signal(signal.SIGALRM, handler)
signal.alarm(3) #Set the parameter to the amount of seconds you want to wait

try:
    socketIO = SocketIO('192.168.0.104', 5000)
    print("SOCKET CONNECTED")
except:
    print("Erro ao Conectar!")
    print("")
signal.alarm(3)


#ds18b20 SETTINGS
 
os.system('modprobe w1-gpio')           #ds18b20 lib
os.system('modprobe w1-therm')
 
base_dir = '/sys/bus/w1/devices/'       #ds18b20 config
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'
 
def read_temp_raw():                    #ds18b20 read function
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines
 
def read_temp():                        #ds18b20 read function           
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

GPIO.setmode(GPIO.BOARD)                #pwm
GPIO.setwarnings(False)

GPIO.setup(32,GPIO.OUT)                 #heater pin 
p = GPIO.PWM(32,60)
p.start(0)


setpoint = 38   #em graus celsius
kP = 60
kI = 0.1
kD = 0.5
potMax=90


tempRead=0                          #variaveis globais q fazem atribuição antes da declaração
I = 0
totalTimer=0
sumAverTemp=0
sumAverPower=0
minTemp=read_temp()
maxTemp=minTemp
power=0

p.ChangeDutyCycle(power)

def main():
    global tempRead
    global I
    global totalTimer
    global sumAverTemp
    global sumAverPower
    global minTemp
    global maxTemp
    global power
    periodicidade = 300              #em segundos

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

    now=datetime.datetime.fromtimestamp(int((time.time()))).strftime('%d-%m-%Y %H:%M:%S')
    data={
        'stamp' : str(now),
        'temp' : str(round(tempRead,1)),
        'power' : str(round(power,1))
        }
    #SOCKET:
    signal.alarm(3)
    #jeison=json.loads(str(data))
    try:
        print(data)
        #socketIO.emit('message',str(data))
        socketIO.emit('ds18b20',data)
        print('Sent: ',round(tempRead,2),"  ",round(power,2),"%")
        print("")
    except:
        print("Erro ao enviar informação!")
        print("")
    signal.alarm(3)
        

    elapsedTime=(time.time())-startTimer
    totalTimer+=elapsedTime
    sumAverTemp+=tempRead*elapsedTime
    sumAverPower+=lastPower*elapsedTime
    
    print(round(totalTimer,2))

    weigAverTemp=sumAverTemp/totalTimer         #essa parte pode passar pra dentro da prox condicional
    weigAverPower=sumAverPower/totalTimer       #essa tambem
    
    #print("delay: ",round(elapsedTime,2)," Total tempo decorrido: ",round(totalTimer,2)," Med. Pond: ",round(weigAverTemp,2), " PowerAver: ",round(weigAverPower,2))
    #print("minTemp: ",round(minTemp,2)," maxTemp: ",round(maxTemp,2))
    #print("DHT: T: ",temperatureDHT1,"H: ",humidityDHT1)
    #print("")

    if (totalTimer >= periodicidade):
        # print("")
        # print("Total Tempo decorrido: ",round(totalTimer,2)," Med. Pond: ", round(weigAverTemp,2))
        # print("minTemp: ",round(minTemp,2)," maxTemp: ",round(maxTemp,2)," Media Pot: ",round(weigAverPower,2))
        # print("")
        signal.alarm(8)
        Tstamp='ds18b20'+'#'+str(int((time.time())))
        print("")
        dynamoFunctions.genericPutKW(partitionKey,Tstamp,TemperatureAverage=weigAverTemp,MinimumTemp=minTemp,MaximumTemp=maxTemp,Power=weigAverPower)
        print("")
        totalTimer=0
        sumAverTemp=0
        sumAverPower=0
        maxTemp=tempRead
        minTemp=tempRead
        
    
        
        
if __name__ == "__main__":

    global partitionKey
    partitionKey='testeSocket'
    while(1):
        main()


