import RPi.GPIO as GPIO
import time
from socketIO_client import SocketIO, LoggingNamespace
from threading import Thread

socketIO = SocketIO('192.168.0.104', 5000,LoggingNamespace)

GPIO.setmode(GPIO.BOARD)
    
controlPin = [23,26,24,22]

t = Thread(target=socketIO.wait(seconds=2))
t.start()


def main():
    #print('main')
    #socketIO.wait(seconds=1)
    #time.sleep(1)
    #event.wait()
    #event.clear()
    #time.sleep(1)
    socketIO.on('rollEggs',on_rollEggs)
    socketIO.wait()
    print("oi")



def teste():
    print('main')
    socketIO.on('aaa_response',on_aaa_response)
    socketIO.emit('message','mensagem')
    socketIO.wait(seconds=1)
    socketIO.emit('aaa','foi')
    socketIO.wait(seconds=1)
        

def rollThem():
    
    for pin in controlPin:
        GPIO.setup(pin,GPIO.OUT)
        GPIO.output(pin,0)
        
    seq= [[1,0,0,0],
          [1,1,0,0],
          [0,1,0,0],
          [0,1,1,0],
          [0,0,1,0],
          [0,0,1,1],
          [0,0,0,1],
          [1,0,0,1]]
    
    counterCWseq= [[0,0,0,1],
                   [0,0,1,1],
                   [0,0,1,0],
                   [0,1,1,0],
                   [0,1,0,0],
                   [1,1,0,0],
                   [1,0,0,0],
                   [1,0,0,1]]
    print("ok, I'll do it")
    time.sleep(6)
    #for i in range(512):
    
    for i in range(380):
        print('counterclockwise')
        for halfStep in range(8):
            for pin in range(4):
                GPIO.output(controlPin[pin],counterCWseq[halfStep][pin])
            time.sleep(0.001)    
    
    for i in range(380):
        print('rodando')
        for halfStep in range(8):
            for pin in range(4):
                GPIO.output(controlPin[pin],seq[halfStep][pin])
            time.sleep(0.001)

    
def on_aaa_response(data):
    print('on_aaa_response',data)
    
def on_rollEggs(data):
    rollThem()
    socketIO.emit('message','Rolou!')
    print('msg: ',data)
    #event.set()

if __name__ == '__main__':

    while(1):
        main()
        
    #rollThem()