# coding: utf8

import os
import glob
import time
import boto3
from datetime import datetime
import sys, getopt
from pprint import pprint

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
    attributes = []
    for key, value in data.iteritems():
        attributes.append({
            'Name': key,
            'Value': value.isoformat() if type(value) is datetime else value,
            'Replace': True
        })

    client.put_attributes(
        DomainName='pilp.logs',
        ItemName=data['time'].isoformat(),
        Attributes=attributes
    )

def get_newest():
    result = client.select(SelectExpression="select * from `pilp.logs` where itemName() like '2016%' order by itemName() desc limit 1")
    pprint(result['Items'])

def get_meta():
    result = client.domain_metadata(
        DomainName='pilp.logs'
    )
    pprint(result)

def read_temp_raw(device_file):
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp(device_file, return_raw=False):
        lines = read_temp_raw(device_file)
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = read_temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
            return temp_string if return_raw else temp_c

def log_sensors():
    data = {
        'time': datetime.today()
    }
    for sensor in sensors:
        data[sensor['name']] = read_temp(base_dir + sensor['device'] + device_file, True)

    store_data(data)

def main(argv = None):
    if argv is None:
        argv = sys.argv

    try:
        if argv[1] == 'init':
            init()
        elif argv[1] == 'show':
            get_newest()
        elif argv[1] == 'meta':
            get_meta()
        else:
            log_sensors()
    except IndexError:
        log_sensors()

if __name__ == "__main__":
    main()
