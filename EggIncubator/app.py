from flask import Flask, render_template, request, url_for, redirect
import boto3
import time

app = Flask(__name__)


dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('EggIncubator')

from boto3.dynamodb.conditions import Key, Attr


@app.route('/')
def login():    
    return render_template('login.html')

@app.route('/check',methods = ['post'])
def check():
    if request.method=='POST':
        
        pkID = request.form['email']
        password = request.form['password']
        
        table = dynamodb.Table('EggIncubator')
        response = table.query(
                KeyConditionExpression=Key('pkID').eq(pkID)
        )
        items = response['Items']
        name = items[0]['name']
        print(items[0]['password'])
        if password == items[0]['password']:
            getPair=graph()
            #return redirect(url_for('graph'))
            return render_template("home.html", labels=getPair[0], values=getPair[1])
            #return render_template("home.html",name = name)
    return render_template("login.html")
    
    
#@app.route('/home')
#def home():
#    return render_template('home.html')

#@app.route("/graph")
def graph():
    
    #Scan
    resp_Scan = table.scan(ProjectionExpression="Tstamp, Temperature")
    
    #print(resp_Scan['Items'])
    
    ScanList=[]    
    for elem in resp_Scan['Items']:
        ScanList.append(elem.values())

    PairedList =[]
    for items in ScanList:
        #print (items)
        #print (len(items))
        if (len(items)) == 2:
            PairedList.append(list(items))
    
    #for i in PairedList:
        #print (len(i))
        #print (i[0],":",i[1])
        
    #print(type(PairedList))
    
    PairedList.sort()  #ordena as informações

    labels = []
    values = []
    for row in PairedList:
        #print (row[0],":",row[1])
        labels.append(str(row[0]))
        values.append(row[1])
       
    return (labels,values)
    #return render_template("home.html", labels=labels, values=values)



if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port="5000")

