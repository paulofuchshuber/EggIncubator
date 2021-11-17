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
    #print(titles)
    splittedData=splitData(titles,resp_Query)

    # for element in splittedData:
    #     print (element)
    # for element in titles:
    #     print (element)

    return (titles,splittedData)
    
def returnTitles(Data):
    titles=[]
    for item in Data:
            for k,v in item.items():
                #print(k,v) 
                titles.append(k)
            #print("")
    titles=set(titles)
    return titles

def splitData(titles,Data):
    
    dataVector= [[] for _ in range(len(titles))]

    print("$$$$$$$$")
    
    for index, item in enumerate(Data):            #Aqui que realmente separa os dados
            # print(index,item)
            # print("")
            for k,v in item.items():
                #print(k,v) 
                n=getKeyIndex(titles,k)
                if (k!="Tstamp" and k!="pkID"):
                    aux=v
                    v={
                        'x': str(treatOneTstamp(item.get('Tstamp'))),
                        'y': str(aux)
                    }
                dataVector[n].append(v)

    # for index, element in enumerate(dataVector):
    #      print(index, element)
    #      print("")
    
    skPosition=getKeyIndex(titles,"Tstamp")         #trata o timestamp
    dataVector[skPosition]=treatTstamp(dataVector[skPosition])
    dataVector[skPosition]=list(set(dataVector[skPosition]))    #remove duplicatas
    dataVector[skPosition].sort()
    
    return dataVector


def getKeyIndex(titles,k):
    #print("(((((")
    for index, item in enumerate(titles):
        if (item==k):
            r=index
            #print(r,item)            
    return r

def treatOneTstamp(data):
    r = data.split("#")
    return r[1]

def treatTstamp(Vector):
    newVector=[]
    for eachTstamp in Vector:
        aux = eachTstamp.split("#")
        newVector.append(aux[1])
        #print(eachTstamp)
    #print(newVector)
    return newVector

def treatDecimal(Vector,Tstamp):
    newVector=[]
    for index,eachItem in enumerate(Vector):
        aux = str(eachItem)
        newVector.append(aux)
        #print(index,aux)
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

