import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('EggIncubator')        

def put(pkID='' , Tstamp='', Temperature='', Humidity=''):  #put into dynamodb
    table = dynamodb.Table('EggIncubator')
    response = table.put_item(
       Item={
            'pkID':pkID,
            'Tstamp' : Tstamp,
            'Temperature':Temperature,
            'Humidity' :Humidity
        }
    )

def callManager(partitionKey):
    manager = table.query(KeyConditionExpression=Key('pkID').eq(partitionKey))['Items']
    managerList=[]
    for elem in manager:
        managerList = elem.get('List')  
        return (managerList)   

def genericPutKW(pkID='' , Tstamp='', Temperature='', Humidity=''):  #put into dynamodb
    table = dynamodb.Table('EggIncubator')
    response = table.put_item(
       Item={
            'pkID':pkID,
            'Tstamp' : Tstamp,
            'Temperature':Temperature,
            'Humidity' :Humidity
        }
    )        

def myfunc(partitionKey,Tstamp,**kwargs):

    print(partitionKey)
    print(Tstamp)
    for k,v in kwargs.items():
        print("%s = %s" % (k, round(v,2)))

# def manyArgs(*arg):
#   print "I was called with", len(arg), "arguments:", arg