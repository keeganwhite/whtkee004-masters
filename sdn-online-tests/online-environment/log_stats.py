# import requests module
import csv
import time

import requests
from requests.auth import HTTPBasicAuth
import json
import pandas as pd

# save numpy array as csv file
from numpy import asarray
from numpy import savetxt


prev = 0
bandwidth_per_device = {}
flow_throughput = {}
packet_loss_per_device = {}


def main():
    # time.sleep(5)
    global flow_throughput
    global bandwidth_per_device
    start = time.time()
    while time.time() - start < 580:
        get_flow_throughput()
        calculate_bandwidth()
        calculate_packet_loss()
        time.sleep(1)
    df_bandwidth = pd.DataFrame([bandwidth_per_device])
    df_bandwidth.to_csv('bandwidth.csv', index=False, header=True)
    df_packet_loss = pd.DataFrame([packet_loss_per_device])
    df_packet_loss.to_csv('packet_loss.csv', index=False, header=True)
    df = pd.DataFrame([flow_throughput])
    df.to_csv('throughput.csv', index=False, header=True)


def get_flow_throughput():
    global prev
    global flow_throughput
    headers = {'Accept': 'application/json'}
    url = 'http://127.0.0.1:8181/onos/v1/flows/of%3A0000000000000001'  # get flow entries from gateway
    rsp = requests.get(headers=headers, url=url, auth=HTTPBasicAuth('onos', 'rocks'))
    rsp_js = rsp.json()
    flows = rsp_js['flows']
    for i in flows:
        try:
            # print(i['selector']['criteria'][2]['mac'])
            mac = i['selector']['criteria'][2]['mac']

            sec = i['life']
            bytes = i['bytes']
            if int(sec) >= 1:
                delta = bytes - prev
                throughput = float((int(delta) / 125) / int(sec))  # kilobits per sec
                if mac in flow_throughput:
                    flow_throughput[mac].append(throughput)
                else:
                    flow_throughput[mac] = [throughput]
                # print(throughput)
                # print('previous before update', prev)
                prev = bytes
                # print('previous after update', prev)
        except Exception:
            continue
    # return int(bytes_received)


def calculate_bandwidth():
    """
    Appends bandwidth per port to device array
    :return: nothing
    """
    global bandwidth_per_device
    headers = {'Accept': 'application/json'}
    url = 'http://127.0.0.1:8181/onos/v1/statistics/delta/ports'
    rsp = requests.get(headers=headers, url=url, auth=HTTPBasicAuth('onos', 'rocks'))
    rsp_js = rsp.json()
    devices = rsp_js['statistics']
    counter = 0
    for device in devices:
        name = device['device']
        # print(switch)
        ports = device['ports']
        for port in ports:
            sent = port['bytesSent']
            received = port['bytesReceived']
            bandwidth = (sent + received) / 125 / port['durationSec']  # kilobits
            if name in bandwidth_per_device:
                bandwidth_per_device[name].append(bandwidth)
            else:
                bandwidth_per_device[name] = [bandwidth]
            # print(bandwidth)


def calculate_packet_loss():
    global packet_loss_per_device
    headers = {'Accept': 'application/json'}
    url = 'http://127.0.0.1:8181/onos/v1/statistics/delta/ports'
    rsp = requests.get(headers=headers, url=url, auth=HTTPBasicAuth('onos', 'rocks'))
    rsp_js = rsp.json()
    devices = rsp_js['statistics']
    for device in devices:
        name = device['device']
        # print(switch)
        ports = device['ports']
        sent = 0
        received = 0
        for port in ports:
            if port['port'] == 1:
                sent = port['packetsSent']
            else:
                received += port['packetsReceived']
        if received != 0:
            packet_loss = ((received - sent) / received) * 100
            if name in packet_loss_per_device:
                packet_loss_per_device[name].append(packet_loss)
            else:
                packet_loss_per_device[name] = [packet_loss]


if __name__ == "__main__":
    main()
