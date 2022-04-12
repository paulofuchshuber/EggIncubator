import boto3
from boto3.dynamodb.conditions import Key
import pandas as pd
import simplejson as json
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
    #print("Inserted: ",Item)
        
def getChartData(partitionKey):

    resp_Query = table.query(KeyConditionExpression=Key('pkID').eq(partitionKey))['Items']

    #print(type(resp_Query),len(resp_Query))
    # print(resp_Query)


    dumps=json.dumps(resp_Query, use_decimal=True)
    #print(type(dumps))
    obj_DF = pd.DataFrame(json.loads(dumps))

    obj_DF=obj_DF.drop(columns=['pkID'])


    obj_DF['Tstamp'] = obj_DF['Tstamp'].str.split('#').str[-1].str.strip()  #remove string before #, ex: DHT22#123123123 = 123123123
    
    obj_DF=obj_DF.sort_values(by=['Tstamp'])
    

    obj_DF['Tstamp'] = (pd.to_datetime(obj_DF['Tstamp'],unit='s')) 
    obj_DF['Tstamp'] = obj_DF['Tstamp'].dt.strftime('%d-%m-%Y %I:%M:%S')
    #print(obj_DF['Tstamp'])
    #print(obj_DF.columns)

    TstampsWoDup=obj_DF['Tstamp'].drop_duplicates()

    TstampsWithoutDuplicates=list(TstampsWoDup)
    #print(TstampsWithoutDuplicates)

    
    orderedPairs=[]
    labels=[]

    pos=0
    for column in obj_DF.columns:
        if column != "Tstamp":
            labels.append(str(column))
            orderedPairs.append(obj_DF[["Tstamp", str(column)]])
            orderedPairs[pos]=orderedPairs[pos].drop_duplicates(subset=["Tstamp"])
            orderedPairs[pos]=orderedPairs[pos].rename(columns={'Tstamp': 'x', str(column): 'y'})
            orderedPairs[pos] = orderedPairs[pos][orderedPairs[pos]["y"].notna()]
            orderedPairs[pos]=orderedPairs[pos].to_dict('records')
            pos+=1

    #print(labels)
   

    return (labels,TstampsWithoutDuplicates,orderedPairs)


def genericQueryData(partitionKey):
    resp_Query = table.query(KeyConditionExpression=Key('pkID').eq(partitionKey))['Items']
    
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

