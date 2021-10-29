# EggIncubator

# Prompt-Command (Windows)

## Requirements:

$py -m venv env #create virtual environment  
$env\Scripts\activate	#activate environment  
$pip install Flask  
$pip install boto3  
$pip install awscli  
$aws configure	#you have to put your credentials here  
$pip install Pillow  
$pip install opencv-python  
$pip install flask-socketio  
$pip install psutil
$pip install flask-wtf 

## Run

$env\Scripts\activate	#activate environment  
$set FLASK_APP=app.py  
$CD EggIncubator  
$flask run --host=0.0.0.0  

# Terminal (Raspberry Pi OS)

## Requirements:

$git clone https://github.com/phfuks/EggIncubator  
$sudo pip install virtualenv #install virtual environment  
$python3 -m venv ./venv #create virtual envoironment  
$source ./venv/bin/activate  
$pip install Flask  
$pip install boto3  
$pip install awscli  
$aws configure	#you have to put your credentials here  
$pip install opencv-python  
$pip install Flask-BasicAuth  
$pip install Pillow  
$pip install picamera  
$sudo apt-get install libatlas-base-dev  
$sudo apt-get install libcblas-dev libhdf5-dev libhdf5-serial-dev libatlas-base-dev libjasper-dev libqtgui4 libqt4-test  
$pip install flask-socketio  

#### DHT Sensor Library:  
$git clone https://github.com/adafruit/Adafruit_Python_DHT.git  
$cd Adafruit_Python_DHT  
$sudo apt-get install build-essential python-dev  
$python setup.py install

## Run

$source ./venv/bin/activate  
$set FLASK_APP=app.py  
$cd EggIncubator  
$flask run --host=0.0.0.0  
