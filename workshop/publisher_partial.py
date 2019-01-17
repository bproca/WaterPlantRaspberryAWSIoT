#!/usr/bin/env python

import paho.mqtt.client as mqtt
from datetime import datetime
import time
import ssl
import os
import json

client_id = 'TODO' # the name of the AWS IoT Thing
thing_endpoint = 'TODO' #aws IoT thing endpoint
mqtt_topic = 'TODO' # the mqtt topic

# certs
cert_filename = 'certs/raspberry-certificate.pem.crt'
ca_filename = 'certs/root-ca.pem'
private_key_filename = 'certs/raspberry-private.pem.key'

# mqtt connection
client = mqtt.Client(client_id=client_id)

def on_disconnect(client, userdata, rc):
    print("Disconnected from AWS IoT")
def on_connect(client, userdata, flags, rc):
    print("Connected to AWS IoT with result code")

def on_log(client, obj, level, string):
    print(string)

def setup():
    client.tls_set(
        ca_filename,
        certfile=cert_filename,
        keyfile=private_key_filename,
        tls_version=ssl.PROTOCOL_TLSv1_2)

    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_log = on_log
    client.connect(thing_endpoint, 8883, 70)
    client.loop_start()


def get_rpi_serial_no():
    cpu_serial = "0000000000000000"
    try:
        f = open('/proc/cpuinfo', 'r')
        for line in f:
            if line[0:6] == 'Serial':
                cpu_serial = line[10:26]
        f.close()
    except:
        cpu_serial = "ERROR000000000"
    print "CPU serial no.%s" %cpu_serial
    return cpu_serial

def get_now():
    now = datetime.now()
    return now.strftime("%y-%m-%dT%H:%M:%S.%f")

# TODO
# create the json object that we want to send
# publish the json to the topic using the mqtt client http://www.steves-internet-guide.com/into-mqtt-python-client/
def send_data(moisture):
    # TODO

