from flask import Flask, render_template, request, url_for, redirect, session, g
import boto3
import time
from boto3.dynamodb.conditions import Key, Attr

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

@app.route('/charts')
def charts():
    print(g.user)
    if g.user is None:
        return redirect(url_for('login'))
    else:
        getPair=getGraphData()
        return render_template("charts.html", labels=getPair[0], values=getPair[1])



def getGraphData():
    
    #Scan
    resp_Scan = table.scan(ProjectionExpression="Tstamp, Temperature")['Items']
    

    ScanList=[]    
    for elem in resp_Scan:
        ScanList.append(elem.values())
    
    PairedList =[]
    for items in ScanList:
        if (len(items)) == 2:
            PairedList.append(list(items))
    
    PairedList.sort()  #ordena as informações

    labels = []
    values = []
    for row in PairedList:
        #print (row[0],":",row[1])
        labels.append(str(row[0]))
        values.append(row[1])
       
    return (labels,values)

@app.route('/forms')
def forms():   
    if g.user is None:
        return redirect(url_for('login'))
    else:
        #your code here    
        return render_template("forms.html")   

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

