import time
import picamera
from socketIO_client import SocketIO
import json 
import base64


try:
    socketIO = SocketIO('192.168.0.104', 5000)
    print("SOCKET CONNECTED")
except:
    print("Erro ao Conectar!")
    print("")

with picamera.PiCamera() as camera:
    camera.start_preview()
    i=0
    while(1):
        #time.sleep(1)
        camera.capture('image.jpg',format='jpeg')
        i+=1
        print('shot',i)
        #socketIO.emit('ds18b20',data)
        with open("image.jpg", "rb") as img:
            image = base64.b64encode(img.read())
            data = image.decode() # not just image
            #print(json.dumps(data))
        socketIO.emit('camera', {'image_data': json.dumps(data)})

    camera.stop_preview()