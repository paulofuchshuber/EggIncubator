try:
    import os
    import sys
    import datetime
    import time
    import boto3
    from boto3.dynamodb.conditions import Key
    import Adafruit_DHT
    import threading
    print("All Modules Loaded ...... ")
except Exception as e:
    print("Error {}".format(e))


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
                'Tstamp' : 'dht11#'+str(Tstamp),
                'Temperature':Temperature,
                'Humidity' :Humidity,
            }
        )
        
    def putExt(self, pkID='' , Tstamp='', TemperatureExt='', HumidityExt=''):
        self.table.put_item(
            Item={
                'pkID':pkID,
                'Tstamp' : 'dht11EXT#'+str(Tstamp),
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

        sensor = Adafruit_DHT.DHT11

        humidity, temperature = Adafruit_DHT.read_retry(sensor, GPIOpin)
        temperature+=37.5
        humidity+=64

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


    pinDHT1=23
    pinDHT2=24
    
    now = int(time.time())
    threading.Timer(interval=60, function=main).start()
    obj = MyDb()
    
    Temperature , Humidity = obj.sensor_value(pinDHT1) 

    TemperatureExt , HumidityExt = obj.sensor_value(pinDHT2)

    deltaTemp=abs(Temperature-lastTemp)
    deltaHumid=abs(Humidity-lastHumid)
    #print (deltaTemp)
    if (now is not None) and (deltaTemp<2.5) and (Temperature < 50) and (Humidity <=100) and (Temperature > 0) and (deltaHumid<5):   #alterar para: se dia e hora for nulo, obter dia e hora, talvez em while...
        obj.put(pkID=partitionKey, Tstamp=str(now), Temperature=str(round(Temperature,3)), Humidity=str(round(Humidity,3)))
        counter = counter + 1
        print("{0:0} - Uploaded Sample on Cloud T:{1:0.1f},H:{2:0.1f} ".format(counter-1, Temperature, Humidity))
    lastTemp=Temperature
    lastHumid=Humidity
    

    deltaTempExt=abs(TemperatureExt-lastTempExt)
    #print (deltaTempExt)
    if (now is not None) and (deltaTempExt<2) and (TemperatureExt < 50) and (HumidityExt <=100) and (TemperatureExt > 0):   #alterar para: se dia e hora for nulo, obter dia e hora, talvez em while...
        obj.putExt(pkID=partitionKey, Tstamp=str(now), TemperatureExt=str(round(TemperatureExt,3)), HumidityExt=str(round(HumidityExt,3)))
        #counter = counter + 1
        print("{0:0} - Uploaded Sample on Cloud T (Ext):{1:0.1f},H:{2:0.1f} ".format(counter-1, TemperatureExt, HumidityExt))
    lastTempExt=TemperatureExt
    
    
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
    partitionKey='teste2NewSortKey'

    checkPartitionKeys()
    print('enter')
    main()









