# import requests module
import time

import requests
from requests.auth import HTTPBasicAuth
import json

prev = 0
s1 = []
s2 = []
s3 = []
s4 = []
s5 = []
s6 = []
arr = [s1, s2, s3, s4, s5, s6]


def main():
    start = time.time()
    while time.time() - start < 500:
        print(get_switches())
        time.sleep(5)


def get_switches():
    switches = []
    url = 'http://127.0.0.1:8181/onos/v1/devices'
    headers = {'Accept': 'application/json'}
    rsp = requests.get(headers=headers, url=url, auth=HTTPBasicAuth('onos', 'rocks'))
    rsp_js = rsp.json()
    devices = rsp_js['devices']
    for device in devices:
        switches.append(device['id'])
    return switches


def meter():
    meter = {
        "deviceId": "of:0000000000000002",
        "unit": "KB_PER_SEC",
        "burst": "false",
        "bands": [
            {
                "type": "DROP",
                "rate": "1000",
                "burstSize": "0",
                "prec": "0"
            }
        ]
    }
    flow = {

    }
    headers = {'user-agent': 'my-app/0.0.1'}
    meter_url = 'http://127.0.0.1:8181/onos/v1/meters/of%3A0000000000000002'
    rsp = requests.post(url=meter_url, json=meter, auth=HTTPBasicAuth('onos', 'rocks'))
    print(rsp.status_code)


def get_bytes_bytes_received(port):
    headers = {'Accept': 'application/json'}
    meter_url = 'http://127.0.0.1:8181/onos/v1/statistics/ports'
    rsp = requests.get(headers=headers, url=meter_url, auth=HTTPBasicAuth('onos', 'rocks'))
    rsp_js = rsp.json()
    bytes_received = rsp_js['statistics'][0]['ports'][port]['bytesReceived']
    print(bytes_received)
    return int(bytes_received)


def get_flow_throughput(mac_address):
    global prev
    headers = {'Accept': 'application/json'}
    url = 'http://127.0.0.1:8181/onos/v1/flows/of%3A0000000000000001'
    rsp = requests.get(headers=headers, url=url, auth=HTTPBasicAuth('onos', 'rocks'))
    rsp_js = rsp.json()
    flows = rsp_js['flows']
    for i in flows:
        try:
            # print(i['selector']['criteria'][2]['mac'])
            mac = i['selector']['criteria'][2]['mac']
            if mac == mac_address:
                sec = i['life']
                bytes = i['bytes']
                if int(sec) - 5 > 0:
                    delta = bytes - prev
                    throughput = float((int(delta) / 125) / 5)  # kilobits per sec
                    print(throughput)
                    print('previous before update', prev)
                    prev = bytes
                    print('previous after update', prev)
                break
        except Exception:
            continue
        else:
            continue
    # return int(bytes_received)


def calculate_bandwidth():
    headers = {'Accept': 'application/json'}
    url = 'http://127.0.0.1:8181/onos/v1/statistics/delta/ports'
    rsp = requests.get(headers=headers, url=url, auth=HTTPBasicAuth('onos', 'rocks'))
    rsp_js = rsp.json()
    devices = rsp_js['statistics']
    counter = 0
    for device in devices:
        switch = arr[counter]
        # print(switch)
        ports = device['ports']
        for port in ports:
            sent = port['bytesSent']
            received = port['bytesReceived']
            bandwidth = (sent + received) / 125 / port['durationSec']
            print(bandwidth)
        counter += 1


def calculate_packet_loss():
    global arr
    headers = {'Accept': 'application/json'}
    url = 'http://127.0.0.1:8181/onos/v1/statistics/delta/ports'
    rsp = requests.get(headers=headers, url=url, auth=HTTPBasicAuth('onos', 'rocks'))
    rsp_js = rsp.json()
    devices = rsp_js['statistics']
    counter = 0
    for device in devices:
        switch = arr[counter]
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
            print(counter)
            packet_loss = ((received - sent) / received) * 100
            switch.append(packet_loss)
            print(packet_loss)
        counter += 1


if __name__ == "__main__":
    main()
