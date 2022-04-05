from socket import socket
from flask import Flask, render_template, request, url_for, redirect, session, g
import boto3
import pandas as pd
import numpy as np
import time
import datetime
from boto3.dynamodb.conditions import Key, Attr
from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from flask_socketio import SocketIO, send, emit
from flask_bootstrap    import Bootstrap
from flask_cors import CORS
import random
import dynamoFunctions
import json 
import base64
from io import BytesIO
from PIL import Image


app = Flask(__name__)
app.secret_key = 'somesecretkey'
socketio = SocketIO(app)

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('EggIncubator')

bootstrap = Bootstrap(app)
CORS(app)

class User:
    def __init__(self, id, user, password):
        self.id = id
        self.name = name
        self.password = password

    def __repr__(self):
        return f'<User: {self.user}>'

@app.before_request
def before_request():
    g.user=None
    if 'user_id' in session: 
        g.user=User
        print('###')
                  

@app.route('/')
def main():    
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():        
    g.user=None
    for key in list(session.keys()):
        session.pop(key)

    if request.method == 'POST':
         
        pkID = request.form['email']
        password = request.form['password']

        if len(pkID) == 0:     #se o campo de login estiver nulo...
            print("#: Digite um Email!")
            return redirect(url_for('login'))

        table = dynamodb.Table('EggIncubator')
        response = table.query(
                KeyConditionExpression=Key('pkID').eq(pkID)
        )
        items = response['Items']

        if len(items) == 0:     #se nao existir nenhum usuário correspondente...
            return redirect(url_for('login'))
    
        if password == items[0]['password']:    #Se conseguiu logar...
            session['user_id']=pkID

            #print(items[0].get('name'))

            User.id=items[0].get('pkID')
            User.name=items[0].get('name')
            User.password=items[0].get('password')
            
            
            print(User.id)
            #print(User.name)
            #print(User.password)

            return redirect(url_for('home'))
        return redirect(url_for('login'))
        
    return render_template('login.html')

@app.route('/home')
def home():
    if g.user is None:
        return redirect(url_for('login'))
    else:
        #your code here
        print('1111111111111111111',session.get('user_id'))      
        return render_template("home.html")   


@app.route('/components', methods=["POST","GET"])
def components(): 
    if g.user is None:
        return redirect(url_for('login'))
    else:
        global randomNumber
        #your code here
        #randomNumber=round(38+(random.random()/10),2)

        global ds18b20Data,dht22Data,dht22extData

        return render_template('components.html', ds18b20Data=ds18b20Data,dht22Data=dht22Data,dht22extData=dht22extData)
  

class chartsForm(FlaskForm):
    selectChart = SelectField('Plot: ', choices=[])

def callManager(partitionKey):
    manager = table.query(KeyConditionExpression=Key('pkID').eq(partitionKey))['Items']
    managerList=[]
    for elem in manager:
        managerList = elem.get('List')  
        return (managerList)    

@app.route('/charts', methods=['GET','POST'])
def charts():
    print(g.user)
    if g.user is None:
        return redirect(url_for('login'))
    else:
        #your code here  

        lastPartitionKey=callManager('KeyManager2')[-1]
        getData = dynamoFunctions.genericQueryData(lastPartitionKey)
        getData2 = dynamoFunctions.getChartData(lastPartitionKey)
         

        form = chartsForm()


        form.selectChart.choices = callManager('KeyManager2')        #form.selectChart.choices = [for choice in callManager()]
        if request.method == 'POST':
            getData = dynamoFunctions.genericQueryData(str(form.selectChart.data))  
            getData2 = dynamoFunctions.getChartData(str(form.selectChart.data))
        
        dataInedexes=[]
        for index,title in enumerate(getData[0]):   
            if (title=="Tstamp"):
                labels=getData[1][index]    #confere em titles qual a posição do timestamp e seta como lables
            elif (title!="pkID"):
                dataInedexes.append(index)  #array que informa os vetores de informações (Y axis)

        titles=[]
        for title in getData[0]:    #legendas, essa caca veio como 'set'
            titles.append(title)

        values=[]
        values=packToChartJS(getData[1],dataInedexes,titles)
        values2=packFromDFToChartJS(getData2[2],getData2[0])

        # for i in values:
        #     print(i)
        #     print()        
        # print("###")
        # print("###")
        # print("###")
        
        # for i in values2:
        #     print(i)
        #     print()
        

        #return render_template("charts.html",labels=labels,values=values, form=form)
        return render_template("charts.html",labels=getData2[1],values=values2, form=form)
        

def packFromDFToChartJS(Data,titles):
    colors={
        'Temperature':['#d9ca00'],
        'Humidity':['#048000'],
        'TemperatureExt':['#be8f6a'],
        'HumidityExt':['#1bf505'],
        'MaximumTemp':['rgba(231, 76, 60, 1)'],
        'TemperatureAverage':['rgba(142, 68, 173, 1)'],
        'MinimumTemp':['rgba(41, 128, 185, 1)'],
        'Power':['rgba(0, 0, 0, 1)']
    }
    result=[]
    n=0
    for i in Data:        
        colorAux=colors.get(titles[n]) or 'rgba(0, 0, 0, 1)'
        #print(titles[i])
        #print("CCCCC:",colorAux)
        #print()
        aux={
            'label': titles[n],
            'data': Data[n],
            'backgroundColor': colorAux,
            'borderColor': colorAux
        }
        result.append(aux)
        n+=1
        #print(aux)
    #print(Data,Indexes)
    return result


def packToChartJS(Data,Indexes,titles):
    colors={
        'Temperature':['#d9ca00'],
        'Humidity':['#048000'],
        'TemperatureExt':['#be8f6a'],
        'HumidityExt':['#1bf505'],
        'MaximumTemp':['rgba(231, 76, 60, 1)'],
        'TemperatureAverage':['rgba(142, 68, 173, 1)'],
        'MinimumTemp':['rgba(41, 128, 185, 1)'],
        'Power':['rgba(0, 0, 0, 1)']
    }
    #print(colors)
    result=[]
    #print("TTTTTTTT", type(colors))
    for i in Indexes:        
        colorAux=colors.get(titles[i]) or 'rgba(0, 0, 0, 1)'
        #print(titles[i])
        #print("CCCCC:",colorAux)
        #print()
        aux={
            'label': titles[i],
            'data': Data[i],
            'backgroundColor': colorAux,
            'borderColor': colorAux
        }
        result.append(aux)
        #print(aux)
    #print(Data,Indexes)
    return result


def getGraphData():
    
    #Scan
    resp_Scan = table.scan(ProjectionExpression="Tstamp, Temperature, Humidity")['Items']

    ScanList=[]    
    for elem in resp_Scan:
        ScanList.append(elem.values())
    
    PairedList =[]
    for items in ScanList:
        if (len(items)) == 3:
            PairedList.append(list(items))
    
    PairedList.sort()  #ordena as informações

    labels = []
    values = []
    valuesAgain=[]
    for row in PairedList:
        #print (row[0],":",row[1])
    #   labels.append(str(row[0]))
        labels.append(str(datetime.datetime.fromtimestamp(row[0])))
        values.append(row[1])
        valuesAgain.append(row[2])
    

    return (labels,values,valuesAgain)

@app.route('/forms', methods=['GET','POST'])
def forms():   
    if g.user is None:
        return redirect(url_for('login'))
    else:
        #your code here  

                
        lastPartitionKey=callManager('KeyManager')[-1]
        myData=getData(lastPartitionKey)


        form = chartsForm()
        form.selectChart.choices = callManager('KeyManager')        #form.selectChart.choices = [for choice in callManager()]
        if request.method == 'POST':
            #print("0000000000", form.selectChart.data)
            #print(type(form.selectChart.data))
            myData = getData(str(form.selectChart.data))
            print(str(form.selectChart.data))
        

        return render_template("forms.html", labels=myData[0],values=myData[1], valuesAgain=myData[2], form=form)

def getData(partitionKey):

    resp_Query = table.query(KeyConditionExpression=Key('pkID').eq(partitionKey))['Items']

    print(type(resp_Query),len(resp_Query))
    # print(resp_Query)

    dumps=json.dumps(resp_Query)
    print(type(dumps))
    obj_DF = pd.DataFrame(json.loads(dumps))

    obj_DF=obj_DF.drop(columns=['pkID'])

    obj_DF['Tstamp'] = (pd.to_datetime(obj_DF['Tstamp'],unit='s')) 
    obj_DF['Tstamp'] = obj_DF['Tstamp'].dt.strftime('%d-%m-%Y %I:%M:%S')
        
    #divide em 2 dataframes e muda os headers
        
    set1 = obj_DF[["Tstamp", "Temperature"]]
    set1 = set1.rename(columns={'Tstamp': 'x', 'Temperature': 'y'})

    set2 = obj_DF[["Tstamp", "Humidity"]]
    set2 = set2.rename(columns={'Tstamp': 'x', 'Humidity': 'y'})

    # transforma em dict
    set1=set1.to_dict('records')
    set2=set2.to_dict('records')
        
    #confere no print
    #print(list(set1))
    # print("!")
    # print("!")
    # print("!")
    #print(list(set2))

    return (list(obj_DF['Tstamp']),list(set1),list(set2))

####ESTA FUNÇÃO ABAIXO ESTÁ OBSOLETA
def queryData(partitionKey):
    resp_Query = table.query(KeyConditionExpression=Key('pkID').eq(partitionKey))['Items']
    

    #print(resp_Query)
    #print(type(resp_Query[0]))
    
    Tstamps=[]
    Temperatures=[]
    Humidities=[]

    for elem in resp_Query:
        Tstamps.append(str(datetime.datetime.fromtimestamp(int(elem.get('Tstamp')))))
        #Tstamps.append(str(datetime.datetime.fromtimestamp(int(elem.get('Tstamp'))+10)))
        # Temperatures.append(elem.get('Temperature'))    
        # Humidities.append(elem.get('Humidity'))    
        HumiditiesAux = {
            'x': str(datetime.datetime.fromtimestamp(int(elem.get('Tstamp')))),
            'y': elem.get('Humidity')
        } 
        Humidities.append(HumiditiesAux)
        TemperaturesAux = {
            'x': str(datetime.datetime.fromtimestamp(int(elem.get('Tstamp')))),
            'y': elem.get('Temperature')
        } 
        Temperatures.append(TemperaturesAux)

    return (Tstamps,Temperatures,Humidities)
    
class PowerState(FlaskForm) :
    rollEggs = SubmitField('LEFT')    
    lampState = SubmitField('OFF')       

@app.route('/settings', methods=["POST","GET"])
def settings(): 
    if g.user is None:
        return redirect(url_for('login'))
    else:
        #your code here     
        currentPage = request.url_rule
        print("start camera:",currentPage)
        socketio.emit('startCamera') 

        global lastImage

        form = PowerState()
        


        if form.validate_on_submit() :

            rule = request.url_rule
            print("+ROTA:",rule.rule)
            value=request.form
            print(value)
            rollValue=request.form.get('rollEggs')
            print(rollValue)
            lampValue=request.form.get('lampState')
            print(lampValue)

            if rollValue == 'LEFT':
                PowerState.rollEggs = SubmitField('RIGHT')
                socketio.emit('rollEggs', 'RIGHT')
            elif rollValue == 'RIGHT':
                PowerState.rollEggs = SubmitField('LEFT')
                socketio.emit('rollEggs', 'LEFT')                
            elif lampValue == 'OFF':
                PowerState.lampState = SubmitField('ON')
                socketio.emit('lamp', 'ON')                
            elif lampValue == 'ON':
                PowerState.lampState = SubmitField('OFF')  
                socketio.emit('lamp', 'OFF')                 
        form = PowerState() 


        return render_template("settings.html",form=form,lastImage=lastImage)      

@app.route('/about')
def about():  
    if g.user is None:
        return redirect(url_for('login'))
    else:
        #your code here    
        return render_template("about.html")   

@socketio.on('message')
def handleMessage(msg):
	print('Message: ' + msg)
	send(msg, broadcast=True)

@socketio.on('ds18b20')
def handle_message(msg):
    global ds18b20Data
    ds18b20Data=msg
    print('ds18b20: ', msg)     
    emit('ds18b20',msg, broadcast=True)   

@socketio.on('DHT22')
def handle_message(msg):
    global dht22Data
    dht22Data=msg
    print('DHT22: ', msg)     
    emit('DHT22',msg, broadcast=True)       

@socketio.on('DHT22ext')
def handle_message(msg):
    global dht22extData
    dht22extData=msg
    print('DHT22ext: ', msg)     
    emit('DHT22ext',msg, broadcast=True)         

@socketio.on('camera')
def handle_message(image):
    global lastImage
    global lastImageTime
    print('IMAGE RECEIVED',type(image.get('image_data')))
    print('')
    reponse=image.get('image_data')
    im = Image.open(BytesIO(base64.b64decode(reponse)))
    lastImage=im
    im.save('static/img/piCameraImage.jpg')

    emit('cameraRefresh', broadcast=True) 

    if(time.time()-lastImageTime>60 and time.time()-lastImageTime<1600000000):    
        print('CAMERA TIMEOUT')
        emit('cameraTimeout')
        lastImageTime=0


@socketio.on('CameraViwed')    
def handle_message(msg):
    global lastImageTime
    lastImageTime=int(time.time())
    print()
    print(msg,lastImageTime)
    print()
    

  

global lastImage
global lastImageTime
lastImageTime=0
lastImage=Image.open('static/img/piCameraImage.jpg')
randomNumber=0
global ds18b20Data
global dht22Data
global dht22extData
ds18b20Data={
    'stamp' : str(0),
    'temp' : str(0),
    'power' : str(0)
    }
dht22Data={
    'stampDHT' : str(0),
    'tempDHT' : str(0),
    'HumidityDHT' : str(0)
    }
dht22extData={
    'stampDHText' : str(0),
    'tempDHText' : str(0),
    'HumidityDHText' : str(0)
    }       

if __name__ == "__main__":
    app.debug = True
    socketio.run(app)
    # from waitress import serve
    # serve(app,host="0.0.0.0", port=5000)
    app.run(host="0.0.0.0", port="5000")
