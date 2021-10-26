try:
    import os
    import sys
    import datetime
    import time
    import boto3
    import Adafruit_DHT
    import threading
    print("All Modules Loaded ...... ")
except Exception as e:
    print("Error {}".format(e))


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
                'Tstamp' : Tstamp,
                'Temperature':Temperature,
                'Humidity' :Humidity,
            }
        )
        
    def putExt(self, pkID='' , Tstamp='', TemperatureExt='', HumidityExt=''):
        self.table.put_item(
            Item={
                'pkID':pkID,
                'Tstamp' : Tstamp,
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

        humidity, temperature = Adafruit_DHT.read_retry(sensor, GPIOpin)
        temperature+=1.2

        if humidity is not None and temperature is not None:
            print('Pin={0:0d} Temp={1:0.1f}*C  Humidity={2:0.1f}%'.format(GPIOpin,temperature, humidity))
        else:
            print('Failed to get reading. Try again!')
        return temperature, humidity
    

def main():
    global counter
    global lastTemp
    global lastTempExt
    
    pinDHT1=23
    pinDHT2=24
    
    now = int(time.time())
    threading.Timer(interval=45, function=main).start()
    obj = MyDb()
    
    Temperature , Humidity = obj.sensor_value(pinDHT1) 

    TemperatureExt , HumidityExt = obj.sensor_value(pinDHT2)

    deltaTemp=abs(Temperature-lastTemp)
    #print (deltaTemp)
    if (now is not None) and (deltaTemp<2.5) and (Temperature < 50) and (Humidity <=100):   #alterar para: se dia e hora for nulo, obter dia e hora, talvez em while...
        obj.put(pkID="teste251021", Tstamp=now, Temperature=str(round(Temperature,3)), Humidity=str(round(Humidity,3)))
        counter = counter + 1
        print("{0:0} - Uploaded Sample on Cloud T:{1:0.1f},H:{2:0.1f} ".format(counter-1, Temperature, Humidity))
    lastTemp=Temperature
    
    #now = int(time.time())
    
    deltaTempExt=abs(TemperatureExt-lastTempExt)
    #print (deltaTempExt)
    if (now is not None) and (deltaTempExt<2) and (TemperatureExt < 50) and (HumidityExt <=100):   #alterar para: se dia e hora for nulo, obter dia e hora, talvez em while...
        obj.putExt(pkID="testeEXT251021", Tstamp=now, TemperatureExt=str(round(TemperatureExt,3)), HumidityExt=str(round(HumidityExt,3)))
        #counter = counter + 1
        print("{0:0} - Uploaded Sample on Cloud T (Ext):{1:0.1f},H:{2:0.1f} ".format(counter-1, TemperatureExt, HumidityExt))
    lastTempExt=TemperatureExt
    
    


if __name__ == "__main__":
    global counter
    counter = 0
    global lastTemp
    global lastTempExt
    lastTemp=0
    lastTempExt=0
    main()









