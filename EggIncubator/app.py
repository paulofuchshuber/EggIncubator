from flask import Flask, render_template, request, url_for, redirect, session, g
import boto3
import time
import datetime
from boto3.dynamodb.conditions import Key, Attr
from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from flask_socketio import SocketIO, send
from flask_bootstrap    import Bootstrap
import dynamoFunctions



app = Flask(__name__)
app.secret_key = 'somesecretkey'
socketio = SocketIO(app)

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('EggIncubator')

bootstrap = Bootstrap(app)

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


class componentsForm(FlaskForm):
    submit = SubmitField('submit')
    submit3 = SubmitField('submit3')

class PowerState(FlaskForm) :
    rollEggs = SubmitField('LEFT')    
    lampState = SubmitField('OFF')   
    

@app.route('/components', methods=["POST","GET"])
def components(): 
    if g.user is None:
        return redirect(url_for('login'))
    else:
        #your code here
        #form = componentsForm()
        form = PowerState()

        if form.validate_on_submit() :

            value=request.form
            print(value)
            rollValue=request.form.get('rollEggs')
            print(rollValue)
            lampValue=request.form.get('lampState')
            print(lampValue)

            if rollValue == 'LEFT':
                PowerState.rollEggs = SubmitField('RIGHT')
                
            elif rollValue == 'RIGHT':
                PowerState.rollEggs = SubmitField('LEFT')
                
            elif lampValue == 'OFF':
                PowerState.lampState = SubmitField('ON')
                
            elif lampValue == 'ON':
                PowerState.lampState = SubmitField('OFF')                    
        form = PowerState()
        return render_template('components.html', form=form)

        # if request.method == "POST":   
        #     print(request.form)
        #     componentsForm.submit3 = SubmitField('ON')
        #     value1=request.form.get('rollEggs')
        #     value2=request.form.get('lampState')
        #     print("8888888888888",value1,value2)     
        #     return render_template("components.html", form=form)    

            # for key, value in request.form.items():
            #     print("key: {0}, value: {1}".format(key, value))  
            #     return render_template("components.html", form=form)  

        # if request.method == 'POST':
        #     print("TESTE POST 1")
        #     value=request.form
        #     print(value)

        #     if value == "rollEggs":
        #         socketio.emit('rollEggs', 'rolou') 
        #         value=[]
        #         print ('ROLAGEM')

        #         # componentsForm.rollEggs = SubmitField('ON')
        #     elif value == "lamp":
        #         value=[]
        #         print ('LAMPADA')
                
    
            
        #return render_template("components.html", form=form)     

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
        'TemperatureExt':['#be8f6a'],
        'HumidityExt':['#1bf505'],
        'MaximumTemp':['rgba(231, 76, 60, 1)'],
        'TemperatureAverage':['rgba(142, 68, 173, 1)'],
        'MinimumTemp':['rgba(41, 128, 185, 1)'],
        'Power':['rgba(0, 0, 0, 1)']
    }
    print(colors)
    result=[]
    #print("TTTTTTTT", type(colors))
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

@socketio.on('message')
def handle_message(message):
    print('received message: ' + str(message))    

@socketio.on('aaa')
def test_connect(mensagem2):
    print("AAAAAAAAAAAAAA", mensagem2)
    socketio.emit('aaa_response', 'voltou')    

if __name__ == "__main__":
    app.debug = True
    socketio.run(app)
    # from waitress import serve
    # serve(app,host="0.0.0.0", port=5000)
    app.run(host="0.0.0.0", port="5000")

