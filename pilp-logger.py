import os
import glob
import time

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

sensors = [
    {'device': '28-0315510034ff', 'name': 'Menovesi'},
    {'device': '28-031550fff1ff', 'name': 'Höyrystin'},
    {'device': '28-0315511b62ff', 'name': 'Kattila'},
    {'device': '28-03155106f8ff', 'name': 'Jäteilma'},
]

base_dir = '/sys/bus/w1/devices/'
device_file = '/w1_slave'

def read_temp_raw(device_file):
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp(device_file):
        lines = read_temp_raw()
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = read_temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
            return temp_c

while True:
    foreach(sensors as sensor):
	   print(device.name + ':' + read_temp(base_dir + sensor.device + device_file))
	time.sleep(1)
