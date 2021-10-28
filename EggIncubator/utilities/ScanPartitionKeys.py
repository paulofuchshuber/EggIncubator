import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('EggIncubator')

resp_Scan = table.scan(ProjectionExpression="pkID")['Items']

ScanList=[]    
for elem in resp_Scan:
    ScanList.append(elem.values())

values=[]
for items in ScanList:
    values.append(list(items))


def remove_duplicates(item_list):
    ''' Removes duplicate items from a list '''
    singles_list = []
    for element in item_list:
        if element not in singles_list:
            singles_list.append(element)
    return singles_list

finalList=remove_duplicates(values)

for eachOne in finalList:
    print(eachOne)