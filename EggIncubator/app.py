from flask import Flask, render_template, request, url_for, redirect, session, g
import boto3
import time
import datetime
from boto3.dynamodb.conditions import Key, Attr
from flask_wtf import FlaskForm
from wtforms import SelectField
import dynamoFunctions

app = Flask(__name__)
app.secret_key = 'somesecretkey'


dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('EggIncubator')



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
        return render_template("home.html")   

@app.route('/components')
def components(): 
    if g.user is None:
        return redirect(url_for('login'))
    else:
        #your code here
        return render_template("components.html")     

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
         

        form = chartsForm()
        form.selectChart.choices = callManager('KeyManager2')        #form.selectChart.choices = [for choice in callManager()]
        if request.method == 'POST':
            getData = dynamoFunctions.genericQueryData(str(form.selectChart.data))  
        
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

        return render_template("charts.html",labels=labels,values=values, form=form)
        
def packToChartJS(Data,Indexes,titles):
    colors={
        'Temperature':['#d9ca00'],
        'Humidity':['#048000'],
        'TemperatureExt':['#a8a032'],
        'HumidityExt':['#058a00'],
        'MaximumTemp':['rgba(231, 76, 60, 1)'],
        'TemperatureAverage':['rgba(142, 68, 173, 1)'],
        'MinimumTemp':['rgba(41, 128, 185, 1)'],
        'Power':['rgba(0, 0, 0, 1)']
    }
    print(colors)
    result=[]
    print("TTTTTTTT", type(colors))
    for i in Indexes:        
        colorAux=colors.get(titles[i]) or 'rgba(0, 0, 0, 1)'
        print(titles[i])
        print("CCCCC:",colorAux)
        aux={
            'label': titles[i],
            'data': Data[i],
            'backgroundColor': colorAux,
            'borderColor': colorAux
        }
        result.append(aux)
        print(aux)
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
        getPair=queryData(lastPartitionKey)

        form = chartsForm()
        form.selectChart.choices = callManager('KeyManager')        #form.selectChart.choices = [for choice in callManager()]
        if request.method == 'POST':
            #print("0000000000", form.selectChart.data)
            #print(type(form.selectChart.data))
            getPair = queryData(str(form.selectChart.data))

        return render_template("forms.html", labels=getPair[0],values=getPair[1], valuesAgain=getPair[2], form=form)

def queryData(partitionKey):
    resp_Query = table.query(KeyConditionExpression=Key('pkID').eq(partitionKey))['Items']
    

    print(resp_Query)
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
    
    

@app.route('/settings')
def settings(): 
    if g.user is None:
        return redirect(url_for('login'))
    else:
        #your code here    
        return render_template("settings.html")      

@app.route('/about')
def about():  
    if g.user is None:
        return redirect(url_for('login'))
    else:
        #your code here    
        return render_template("about.html")   

if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port="5000")

