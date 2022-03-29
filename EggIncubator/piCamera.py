from cProfile import run
import multiprocessing
from multiprocessing.dummy import Process
import time
from multiprocessing import process
import picamera
from socketIO_client import SocketIO
import json 
import base64



try:
    socketIO = SocketIO('192.168.0.240', 80)
    print("SOCKET CONNECTED")
except:
    print("Erro ao Conectar!")
    print("")


def sendImage():       

    with picamera.PiCamera() as camera:
        camera.start_preview()
        i=0

        while(run):

            camera.capture('piCameraShot.jpg',format='jpeg')
            i+=1
            print('shot',i)
            #socketIO.emit('ds18b20',data)
            with open("piCameraShot.jpg", "rb") as img:
                image = base64.b64encode(img.read())
                data = image.decode() # not just image
                #print(json.dumps(data))
            socketIO.emit('camera', {'image_data': json.dumps(data)})

        camera.stop_preview()
        

def startProcess():
    global run
    if (run==0):
        run=1
        print ('start')
        sendProcess=Process(target=sendImage)
        sendProcess.start()
        
    

def stopProcess():
    print ('stop PLEASE')
    global run
    run=0
        

def main():
#    sendProcess=Process(target=sendImage)
    global run
    run=0
    socketIO.on('cameraTimeout', stopProcess)
    socketIO.on('startCamera', startProcess)
    socketIO.wait() 


if __name__ == '__main__':
    

    while(1):
        main()
       
