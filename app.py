import os
import glob
import time
from  datetime import datetime
import math

import sender

import psicrometro

 
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
 
base_dir = '/sys/bus/w1/devices/'
# device_folder = glob.glob(base_dir + '28*')[0]
# device_file = device_folder + '/w1_slave'
 
def read_temp_raw(_device):
    f = open(_device, 'r')
    lines = f.readlines()
    f.close()
    return lines
 
def read_temp(_device):
    lines = read_temp_raw(_device)
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c, temp_f



	
import bme280

data = {
    'temp1' : 0.0,
    'temp2' : 0.0,
    'humidity' : 0.0,
    'tempBMP' : 0.0,
    'pressure' : 0.0,
    'humidityBMP' : 0.0
}

# f = open('tbs.csv', 'a')
# g = open('tbu.csv', 'a')
# h1 = open('humidity.csv', 'a')
# h2 = open('humidityBMP.csv', 'a')

arquivo = open('./data.csv','a')

while True:
    # Get values
    temperature,pressure,humidity = bme280.readBME280All()

    data['tempBMP'] = temperature
    data['pressure'] = round(pressure/10.0,2)
    data['humidityBMP'] = round(humidity+10.0,2)

    try:
        data['temp1'] = read_temp('/sys/bus/w1/devices/28-0517608769ff/w1_slave')[0]
    except:
        data['temp1'] = 0.0
        print("Dry bulb have a problem!")
    try:
        data['temp2'] = read_temp('/sys/bus/w1/devices/28-0517602c44ff/w1_slave')[0]
    except:
        data['temp2'] = 0.0
        print("Wet bulb have a problem! ")

    data['humidity'] = round(psicrometro.ur(data['temp1'],data['temp2'],data['pressure']),2)


    # f.write(str(data['temp1']) + ';')
    # g.write(str(data['temp2']) + ';')
    # h1.write(str(data['humidity']) + ';')
    # h2.write(str(data['humidityBMP']) + ';')

    arquivo = open('./data.csv','a')

    # arquivo.write(str(datetime.now()) + ',')
    arquivo.write(str(int(time.time())) + ',')
    arquivo.write(str(data['temp1']) + ',')
    arquivo.write(str(data['temp2']) + ',')
    arquivo.write(str(data['humidity']) + ',')
    arquivo.write(str(data['humidityBMP']))
    arquivo.write('\n')

    arquivo.close()

    # Ponto de Orvalho
    # print(round(psicrometro.Dew_point(data['temp1'],data['temp2'],data['pressure']),2))

    # Send values to socketio server
    sender.sendData(data)

    time.sleep(0.1)

