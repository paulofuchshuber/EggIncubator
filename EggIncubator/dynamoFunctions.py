import boto3
from boto3.dynamodb.conditions import Key
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('EggIncubator')        



def callManager(partitionKey):
    manager = table.query(KeyConditionExpression=Key('pkID').eq(partitionKey))['Items']
    managerList=[]
    for elem in manager:
        managerList = elem.get('List')  
        return (managerList)   

def genericPutKW(pkID,Tstamp,**kwargs):  #put into dynamodb
    Item={
        'pkID':pkID,
        'Tstamp' : Tstamp
        }
    for k,v in kwargs.items():
        Item[k]=round(Decimal(v),2)
    table = dynamodb.Table('EggIncubator')
    response = table.put_item(Item=Item)
    print("Inserted: ",Item)
        
def genericQueryData(partitionKey):
    resp_Query = table.query(KeyConditionExpression=Key('pkID').eq(partitionKey))['Items']
    return (resp_Query)
    
def returnTitles(Data):
    titles=[]
    for k,v in Data[0].items():
        titles.append(k)
    #print("BBB : ", titles)
    return titles

def splitData(titles,Data):
    

    dataVector= [[] for _ in range(len(titles))]

    # print("$$$$$$$$$$")
    # for n in dataVector:
    #     n.append("1")
    # print(dataVector)

    print("$$$$$$$$")
    
    for index, item in enumerate(Data):
            for k,v in item.items():
                print(k,v) 
                n=getKeyIndex(titles,k)
                dataVector[n].append(v)
            print("")

    #print(dataVector)

    for element in dataVector:
        print(element)
        print("")

    PkSkIndexes=getPkSkIndexes(titles)
    print("P S :",PkSkIndexes)
    
    # #print(Data)
    # for index, item in enumerate(Data):
    #     for k,v in item.items():
    #         #print(k,v) 
    #         for i,n in enumerate(titles):
    #             if n == k:
    #                 dataVector[i]=v
    #                 print(n)#armazena no respectivo vetor
    #     #print(index,item)
    #     print("")
    
    # print(dataVector)


    return dataVector

def getPkSkIndexes(titles):
    for index, item in enumerate(titles):
        if (item=='pkID'):
            p=index
        elif (item=='Tstamp'):
            s=index
        print(index, item)            
    return p,s

def getKeyIndex(titles,k):
    for index, item in enumerate(titles):
        if (item==k):
            r=index
        print(index, item)            
    return r

    # Tstamps=[]
    # Temperatures=[]
    # Humidities=[]
    # for elem in resp_Query:
    #     Tstamps.append(str(datetime.datetime.fromtimestamp(int(elem.get('Tstamp')))))
    #     #Tstamps.append(str(datetime.datetime.fromtimestamp(int(elem.get('Tstamp'))+10)))
    #     # Temperatures.append(elem.get('Temperature'))    
    #     # Humidities.append(elem.get('Humidity'))    
    #     HumiditiesAux = {
    #         'x': str(datetime.datetime.fromtimestamp(int(elem.get('Tstamp')))),
    #         'y': elem.get('Humidity')
    #     } 
    #     Humidities.append(HumiditiesAux)
    #     TemperaturesAux = {
    #         'x': str(datetime.datetime.fromtimestamp(int(elem.get('Tstamp')))),
    #         'y': elem.get('Temperature')
    #     } 
    #     Temperatures.append(TemperaturesAux)

    # return (Tstamps,Temperatures,Humidities)

# def myfunc(partitionKey,Tstamp,**kwargs):

#     print(partitionKey)
#     print(Tstamp)
#     for k,v in kwargs.items():
#         print("%s = %s" % (k, round(v,2)))

# def manyArgs(*arg):
#   print "I was called with", len(arg), "arguments:", arg

# def put(pkID='' , Tstamp='', Temperature='', Humidity=''):  #put into dynamodb
#     table = dynamodb.Table('EggIncubator')
#     response = table.put_item(
#        Item={
#             'pkID':pkID,
#             'Tstamp' : Tstamp,
#             'Temperature':Temperature,
#             'Humidity' :Humidity
#         }
#     )