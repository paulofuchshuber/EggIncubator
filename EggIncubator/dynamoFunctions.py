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
    print("000000000000000000000000000000000000")
    titles=returnTitles(resp_Query)
    print(titles)
    splittedData=splitData(titles,resp_Query)
    return (titles,splittedData)
    
def returnTitles(Data):
    titles=[]
    for k,v in Data[0].items():
        titles.append(k)
    #print("BBB : ", titles)
    return titles

def splitData(titles,Data):
    
    dataVector= [[] for _ in range(len(titles))]

    print("$$$$$$$$")
    
    for index, item in enumerate(Data):            #Aqui que realmente separa os dados
            for k,v in item.items():
                print(k,v) 
                n=getKeyIndex(titles,k)
                dataVector[n].append(v)
    
    skPosition=getKeyIndex(titles,"Tstamp")         #trata o timestamp
    dataVector[skPosition]=treatTstamp(dataVector[skPosition])

    for index, item in enumerate(dataVector):       #trata os demais dados
        if(index!=getKeyIndex(titles,"Tstamp") and index!=getKeyIndex(titles,"pkID")):
            dataVector[index]=treatDecimal(dataVector[index])
            # print(index)

    # for element in dataVector:
    #      print(element)
    #      print("")

    return dataVector


def getKeyIndex(titles,k):
    for index, item in enumerate(titles):
        if (item==k):
            r=index
        #print(index, item)            
    return r

def treatTstamp(Vector):
    newVector=[]
    for eachTstamp in Vector:
        aux = eachTstamp.split("#")
        newVector.append(aux[1])
        #print(eachTstamp)
    #print(newVector)
    return newVector

def treatDecimal(Vector):
    newVector=[]
    for eachItem in Vector:
        aux = str(eachItem)
        newVector.append(aux)
    return newVector


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

