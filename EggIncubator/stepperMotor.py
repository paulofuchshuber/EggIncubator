import RPi.GPIO as GPIO
import time
from socketIO_client import SocketIO, LoggingNamespace
from threading import Thread
import random

socketIO = SocketIO('192.168.0.104', 5000,LoggingNamespace)

GPIO.setmode(GPIO.BOARD)
    
controlPin = [23,26,24,22]
for pin in controlPin:
    GPIO.setup(pin,GPIO.OUT)
    GPIO.output(pin,0)

t = Thread(target=socketIO.wait(seconds=2))
t.start()


def main():
    socketIO.on('rollEggs',on_rollEggs)
    socketIO.wait()
    
    #randomNumber=round(38+(random.random()/10),2)
    #socketIO.emit('randomNumber',randomNumber)
    #time.sleep(2)
    #print("Sent: ",randomNumber)    
        
def rollThemCCW():
    counterCWseq= [[0,0,0,1],
                   [0,0,1,1],
                   [0,0,1,0],
                   [0,1,1,0],
                   [0,1,0,0],
                   [1,1,0,0],
                   [1,0,0,0],
                   [1,0,0,1]]
    print("ok, I'll do it")
    time.sleep(3)
    
    for i in range(380):
        print('counterclockwise')
        for halfStep in range(8):
            for pin in range(4):
                GPIO.output(controlPin[pin],counterCWseq[halfStep][pin])
            time.sleep(0.001)        

def rollThemCW():
    CWseq= [[1,0,0,0],
          [1,1,0,0],
          [0,1,0,0],
          [0,1,1,0],
          [0,0,1,0],
          [0,0,1,1],
          [0,0,0,1],
          [1,0,0,1]]
    print("ok, I'll do it")
    time.sleep(3)
    #for i in range(512):
    for i in range(380):
        print('rodando')
        for halfStep in range(8):
            for pin in range(4):
                GPIO.output(controlPin[pin],CWseq[halfStep][pin])
            time.sleep(0.001)
    

def on_rollEggs(data):
    if data == 'RIGHT':
        rollThemCW()
    elif data == 'LEFT':
        rollThemCCW()
    print('msg: ',data)
    socketIO.emit('message','Rolou')
    #event.set()
    

if __name__ == '__main__':
    print('calibrando...')
    rollThemCW()
    position='RIGHT'
    print('feito')
    while(1):
        main()
        
    #rollThem()