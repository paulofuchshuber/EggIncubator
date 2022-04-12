# EggIncubator

O protótipo utiliza a técnica de controle PID para controlar a temperatura da incubadora e armazena os dados coletados num banco de dados ao longo do tempo. Através de
uma interface gráfica com o usuário, os mesmos dados sensoriais são apresentados graficamente (temperatura, umidade e nível de gases) ao longo do tempo para rápida inspeção e identificação de instabilidades ou condições de ambiente adversas. Na implementação foi utilizado software livre e hardware de baixo custo para construir um protótipo funcional como prova de conceito visando o mercado de pequenos criadores. Com este protótipo foram realizados experimentos empíricos para avaliar o funcionamento do dispositivo e viabilidade da solução proposta.


## Prompt-Command (Windows)

### Requirements:

$py -m venv env #create virtual environment  
$env\Scripts\activate	#activate environment   
$CD EggIncubator  
$pip install -r requirements.txt  
$aws configure	#you have to put your credentials here  

### Run

$env\Scripts\activate	#activate environment  
$set FLASK_APP=app.py  
$CD EggIncubator\EggIncubator  
$flask run --host=0.0.0.0 --port 80  

## Terminal (Raspberry Pi OS)

### Requirements:

$git clone https://github.com/phfuks/EggIncubator  
$sudo pip install virtualenv #install virtual environment  
$python3 -m venv ./venv #create virtual envoironment  
$source ./venv/bin/activate  
$cd EggIncubator  
$pip install -r requirements.txt  
$aws configure	#you have to put your credentials here  

#### DHT Sensor Library:  
$git clone https://github.com/adafruit/Adafruit_Python_DHT.git  
$cd Adafruit_Python_DHT  
$sudo apt-get install build-essential python-dev  
$python setup.py install

### Run

$source ./venv/bin/activate  
$cd EggIncubator/EggIncubator  
$python applicationName.py
