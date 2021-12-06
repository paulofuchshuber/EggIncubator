try:
    import os
    import sys
    import datetime
    import time
    import boto3
    from boto3.dynamodb.conditions import Key
    import Adafruit_DHT
    import threading
    from socketIO_client import SocketIO
    import signal
    print("All Modules Loaded ...... ")
except Exception as e:
    print("Error {}".format(e))

#SOCKET SETTINGS
def handler(signum, frame):
    print('Action took too much time')
    raise Exception('Action took too much time')
    

# signal.signal(signal.SIGALRM, handler)
# signal.alarm(60) #Set the parameter to the amount of seconds you want to wait

try:
    socketIO = SocketIO('192.168.0.104', 5000)
    print("SOCKET CONNECTED")
except:
    print("Erro ao Conectar!")
    print("")


dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('EggIncubator')

class MyDb(object):

    def __init__(self, Table_Name='EggIncubator'):
        self.Table_Name=Table_Name

        self.db = boto3.resource('dynamodb')
        self.table = self.db.Table(Table_Name)

        self.client = boto3.client('dynamodb')

    @property
    def get(self):
        response = self.table.get_item(
            Key={
                'pkID':"1"
            }
        )

        return response

    def put(self, pkID='' , Tstamp='', Temperature='', Humidity=''):
        self.table.put_item(
            Item={
                'pkID':pkID,
                'Tstamp' : 'dht22#'+str(Tstamp),
                'Temperature':Temperature,
                'Humidity' :Humidity,
            }
        )
        
    def putExt(self, pkID='' , Tstamp='', TemperatureExt='', HumidityExt=''):
        self.table.put_item(
            Item={
                'pkID':pkID,
                'Tstamp' : 'dht22EXT#'+str(Tstamp),
                'TemperatureExt':TemperatureExt,
                'HumidityExt' :HumidityExt,
            }
        )

    def delete(self,pkID=''):
        self.table.delete_item(
            Key={
                'pkID': pkID
            }
        )

    def describe_table(self):
        response = self.client.describe_table(
            TableName='EggIncubator'
        )
        return response

    @staticmethod
    def sensor_value(GPIOpin):

        sensor = Adafruit_DHT.DHT22
        sensor2 = Adafruit_DHT.DHT11
        
        humidity, temperature = Adafruit_DHT.read_retry(sensor, GPIOpin)
        #humidity, temperature = (0,0)
        #temperature+=37.8
        #humidity+=65

        if humidity is not None and temperature is not None:
            print('Pin={0:0d} Temp={1:0.1f}*C  Humidity={2:0.1f}%'.format(GPIOpin,temperature, humidity))
        else:
            print('Failed to get reading. Try again!')
        return temperature, humidity

def table_insert(keysList):

    table = dynamodb.Table('EggIncubator')
    response = table.put_item(
       Item={
            'pkID': 'KeyManager2',
            'Tstamp': '1',
            'List': keysList
        }
    )
    #print("inserted")
    return response    
    

def main():
    global counter
    global lastTemp
    global lastTempExt
    global lastHumid
    global partitionKey

    timeinterval=30
    timeout=60

    #signal.alarm(timeout)
    pinDHT1=23
    pinDHT2=24
    
    now = int(time.time())
    threading.Timer(interval=timeinterval, function=main).start()
    obj = MyDb()
    
    Temperature , Humidity = obj.sensor_value(pinDHT1) 
    #signal.alarm(timeout)
    TemperatureExt , HumidityExt = obj.sensor_value(pinDHT2)
    #signal.alarm(timeout)

    deltaTemp=abs(Temperature-lastTemp)
    deltaHumid=abs(Humidity-lastHumid)
    #print (deltaTemp)
    if (now is not None) and (deltaTemp<2.5) and (Temperature < 50) and (Humidity <=100) and (Temperature > 0) and (deltaHumid<5):   #alterar para: se dia e hora for nulo, obter dia e hora, talvez em while...
        #obj.put(pkID=partitionKey, Tstamp=str(now), Temperature=str(round(Temperature,3)), Humidity=str(round(Humidity,3)))
        counter = counter + 1
        print("{0:0} - Uploaded Sample on Cloud T:{1:0.1f},H:{2:0.1f} ".format(counter-1, Temperature, Humidity))
        #signal.alarm(timeout)
        data={
        'stampDHT' : str(datetime.datetime.fromtimestamp(now).strftime('%d-%m-%Y %H:%M:%S')),
        'tempDHT' : str(round(Temperature,1)),
        'HumidityDHT' : str(round(Humidity,1))
        }
        try:
            socketIO.emit('DHT22',data)
        except:
            print("Erro ao enviar informação!")
            print("")
    lastTemp=Temperature
    lastHumid=Humidity
    #signal.alarm(timeout)

    deltaTempExt=abs(TemperatureExt-lastTempExt)
    #print (deltaTempExt)
    if (now is not None) and (deltaTempExt<2) and (TemperatureExt < 50) and (HumidityExt <=100) and (TemperatureExt > 0):   #alterar para: se dia e hora for nulo, obter dia e hora, talvez em while...
        #obj.putExt(pkID=partitionKey, Tstamp=str(now), TemperatureExt=str(round(TemperatureExt,3)), HumidityExt=str(round(HumidityExt,3)))
        #counter = counter + 1
        print("{0:0} - Uploaded Sample on Cloud T (Ext):{1:0.1f},H:{2:0.1f} ".format(counter-1, TemperatureExt, HumidityExt))
        #signal.alarm(timeout)
        data={
        'stampDHText' : str(datetime.datetime.fromtimestamp(now).strftime('%d-%m-%Y %H:%M:%S')),
        'tempDHText' : str(round(TemperatureExt,1)),
        'HumidityDHText' : str(round(HumidityExt,1))
        }        
        try:
            socketIO.emit('DHT22ext',data)
        except:
            print("Erro ao enviar informação!")
            print("")        
    lastTempExt=TemperatureExt
    #signal.alarm(timeout+timeinterval)
    
def checkPartitionKeys():
    existence=0
    manager = table.query(KeyConditionExpression=Key('pkID').eq('KeyManager2'))['Items']
    
    #print (manager)
    managerList=[]
    for elem in manager:
        managerList = elem.get('List')

    for eachElem in managerList:
        if (partitionKey == eachElem):
            #print('true')
            existence=1

    if (existence==0):
        managerList.append(partitionKey)
        item_insert = table_insert(managerList)
        print('pkID added to list')
        #print(item_insert)        

    elif (existence ==1):
        print('Continued on same pkId')

    print(managerList)

if __name__ == "__main__":
    global counter
    counter = 0
    global lastTemp
    global lastTempExt
    lastTemp=0
    lastTempExt=0
    global lastHumid
    lastHumid=0
    global partitionKey
    partitionKey='testeSocket'

    checkPartitionKeys()
    print('enter')
    main()









