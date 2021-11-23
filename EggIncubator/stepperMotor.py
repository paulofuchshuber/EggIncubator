import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

controlPin = [23,26,24,22]

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

for i in range(512):
    print('rodando')
    for halfStep in range(8):
        for pin in range(4):
            GPIO.output(controlPin[pin],seq[halfStep][pin])
        time.sleep(0.001)

GPIO.cleanup()