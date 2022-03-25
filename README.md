# EggIncubator

O protótipo utiliza a técnica de controle PID para controlar a temperatura da incubadora e armazena os dados coletados num banco de dados ao longo do tempo. Através de
uma interface gráfica com o usuário, os mesmos dados sensoriais são apresentados graficamente (temperatura, umidade e nível de gases) ao longo do tempo para rápida inspeção e identificação de instabilidades ou condições de ambiente adversas. Na implementação foi utilizado software livre e hardware de baixo custo para construir um protótipo funcional como prova de conceito visando o mercado de pequenos criadores. Com este protótipo foram realizados experimentos empíricos para avaliar o funcionamento do dispositivo e viabilidade da solução proposta.


## Prompt-Command (Windows)

### Requirements:

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
$pip install flask-socketio  
$pip install eventlet  
$pip install gevent-websocket  
$pip install Flask-Bootstrap  

### Run

$env\Scripts\activate	#activate environment  
$set FLASK_APP=app.py  
$CD EggIncubator\EggIncubator  
$flask run --host=0.0.0.0  

## Terminal (Raspberry Pi OS)

### Requirements:

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
$pip install RPi.GPIO  
$pip install socketIO-client-2  
$pip install flask-socketio  
$pip install eventlet  
$pip install picamera  

#### DHT Sensor Library:  
$git clone https://github.com/adafruit/Adafruit_Python_DHT.git  
$cd Adafruit_Python_DHT  
$sudo apt-get install build-essential python-dev  
$python setup.py install

### Run

$source ./venv/bin/activate  
$cd EggIncubator/EggIncubator  
$python applicationName.py
