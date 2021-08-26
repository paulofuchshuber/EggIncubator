


# Example using a Raspberry Pi with DHT sensor
# connected to GPIO23.




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
    def sensor_value():

        pin = 4
        sensor = Adafruit_DHT.DHT22

        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

        if humidity is not None and temperature is not None:
            print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
        else:
            print('Failed to get reading. Try again!')
        return temperature, humidity


def main():
    global counter
    now = int(time.time())
    threading.Timer(interval=6, function=main).start()
    obj = MyDb()
    Temperature , Humidity = obj.sensor_value()
    if now is not None:   #alterar para: se dia e hora for nulo, obter dia e hora, talvez em while...
        obj.put(pkID="Teste2", Tstamp=now, Temperature=str(round(Temperature,3)), Humidity=str(round(Humidity,3)))
        counter = counter + 1
        print("{0:0} - Uploaded Sample on Cloud T:{1:0.1f},H:{2:0.1f} ".format(counter-1, Temperature, Humidity))


if __name__ == "__main__":
    global counter
    counter = 0
    main()









