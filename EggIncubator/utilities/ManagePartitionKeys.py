import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('EggIncubator')
#table = boto3.resource('dynamodb').Table('EggIncubator')


def callManager():
    manager = table.query(KeyConditionExpression=Key('pkID').eq('KeyManager'))['Items']
    managerList=[]
    for elem in manager:
        managerList = elem.get('List')  

        return (managerList)




def table_insert(keysList):

    table = dynamodb.Table('EggIncubator')
    response = table.put_item(
       Item={
            'pkID': 'KeyManager',
            'Tstamp': "1",
            'List': keysList
        }
    )
    return response


def main():
    keysList=['Teste','Teste2','Teste3','Teste4','Teste5','teste1PID', 'teste231021','teste251021','testeEXT251021','teste261021','teste281021','2teste281021']
    otherList=['testeEXT251021','testeEXT261021','testeEXT281021']
    #'3teste281021'
    #item_insert = table_insert(keysList)
    
    print("Put  succeeded:")
    #print(item_insert)
    
    print("")
    print("Now lets get it:")
    test=callManager()
    print(test)

if __name__ == '__main__':

    main()