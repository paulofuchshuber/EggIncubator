# EggIncubator

# Prompt-Command (Windows)

$py -m venv env #install virtual environment

$env\Scripts\activate	#activate environment

$pip install Flask

$pip install boto3

$pip install awscli

$aws configure	#put your credentials here

$set FLASK_APP=app.py

$pip install Pillow

$pip install opencv-python

$CD EggIncubator

$flask run --host=0.0.0.0

# Terminal (Raspberry Pi OS)

## Requirements:

$git clone https://github.com/phfuks/EggIncubator

$sudo pip install virtualenv #install virtual environment

$python3 -m venv ./venv #create virtual envoironment

$source ./venv/bin/activate

$pip install Flaskaws configure

$pip install boto3

$pip install awscli

$aws configure	#put your credentials here

$set FLASK_APP=app.py

$pip install opencv-python

$sudo apt-get install libatlas-base-dev

$sudo apt-get install libcblas-dev libhdf5-dev libhdf5-serial-dev libatlas-base-dev libjasper-dev libqtgui4 libqt4-test

$pip install Flask-BasicAuth

$pip install Pillow

$pip install picamera

###DHT sensor library:  
$git clone https://github.com/adafruit/Adafruit_Python_DHT.git  
$cd Adafruit_Python_DHT  
$sudo apt-get install build-essential python-dev  

$python setup.py install

$CD EggIncubator

$flask run --host=0.0.0.0
