import RPi.GPIO as GPIO
import time
from socketIO_client import SocketIO, LoggingNamespace

socketIO = SocketIO('192.168.0.104', 5000,LoggingNamespace)

GPIO.setmode(GPIO.BOARD)
    
controlPin = [23,26,24,22]

def main():
    
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
    
    GPIO.cleanup()
    
def on_aaa_response(data):
    print('on_aaa_response',data)

if __name__ == '__main__':
    

    print('oi')

    socketIO.on('aaa_response',on_aaa_response)
    socketIO.emit('message','mensagem')
    socketIO.wait(seconds=1)
    socketIO.emit('aaa','foi')
    socketIO.wait(seconds=1)
    
    socketIO.disconnect()
    #main()