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
