import RPi.GPIO as GPIO
import time as delay

GPIO.setmode(GPIO.BOARD)
GPIO.setup(37,GPIO.OUT) #humidif. pin
i=0


#GPIO.output(37,GPIO.LOW)
#delay.sleep(3)
GPIO.output(37,GPIO.LOW)
print("LOW")
delay.sleep(2)

GPIO.output(37,GPIO.HIGH)
print("HIGH")
delay.sleep(2)

print("DONE!")
