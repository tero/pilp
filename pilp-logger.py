# coding: utf8

import os
import glob
import time
import boto3
from datetime import datetime
import sys, getopt

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

sensors = [
    {'device': '28-0315510034ff', 'name': 'outgoing water'}, #menovesi
    {'device': '28-031550fff1ff', 'name': 'evaporator'}, #höyrystin
    {'device': '28-0315511b62ff', 'name': 'boiler'}, #kattila
    {'device': '28-03155106f8ff', 'name': 'exhaust'}, #jäteilma
]

base_dir = '/sys/bus/w1/devices/'
device_file = '/w1_slave'

client = boto3.client('sdb')

def init():
    client.create_domain(
        DomainName='pilp.logs'
    )

def store_data(data):
    client.put_attributes(
        DomainName='pilp.logs',
        ItemName=data['time'],
        Attributes=[
            data,
        ]
    )

def read_temp_raw(device_file):
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp(device_file):
        lines = read_temp_raw(device_file)
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = read_temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
            return temp_c

def log_sensors():
    data = {
        'time': datetime.today()
    }
    for sensor in sensors:
        data[sensor['name']] = read_temp(base_dir + sensor['device'] + device_file)

    store_data(data)

def main(argv = None):
    if argv is None:
        argv = sys.argv

    try:
        if argv[1] == 'init':
            init()
        else:
            log_sensors()
    except IndexError:
        log_sensors()

if __name__ == "__main__":
    main()
