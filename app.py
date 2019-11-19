import os
import glob
import time
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

while True:
    # for device_folder in glob.glob(base_dir + '28*'):
    #     device_file = device_folder+ '/w1_slave'
    #     print (device_file)


    temperature,pressure,humidity = bme280.readBME280All()

    # print ("Temperature : ", temperature, "C")
    # print ("Pressure : ", pressure, "hPa")
    # print ("Humidity : ", humidityBMP, "%")

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

    # data['humidity'] = psychropy.Rel_hum3(25.0,19.0,data['pressure'])
    # data['humidity'] = psychropy.Rel_hum3(data['temp1'],data['temp2'],data['pressure'])
    data['humidity'] = round(psicrometro.ur(data['temp1'],data['temp2'],data['pressure']),2)

    # Ponto de Orvalho
    # print(round(psicrometro.Dew_point(data['temp1'],data['temp2'],data['pressure']),2))

    sender.sendData(data)

    time.sleep(0.1)

