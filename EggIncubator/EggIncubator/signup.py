from flask import Flask, render_template, request
#import key_config as keys
import boto3
import time

app = Flask(__name__)


dynamodb = boto3.resource('dynamodb')

from boto3.dynamodb.conditions import Key, Attr

@app.route('/')
def index():
    return render_template('signup.html')


@app.route('/signup', methods=['post'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        pkID = request.form['email']
        password = request.form['password']
        Tstamp = int(time.time())
        
        table = dynamodb.Table('EggIncubator')
        
        table.put_item(
                Item={
        'name': name,
        'pkID': pkID,
        'Tstamp' :  Tstamp,
        'password': password
            }
        )
        msg = "Registration Complete. Please Login to your account !"
    
        return render_template('login.html',msg = msg)
    return render_template('signup.html')

@app.route('/login')
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
            
            return render_template("home.html",name = name)
    return render_template("login.html")
@app.route('/home')
def home():
    return render_template('home.html')





if __name__ == "__main__":
    app.run(host="0.0.0.0")
    app.run(debug=True)

