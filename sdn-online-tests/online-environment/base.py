import csv
import random

from scapy.all import *
from classification_model import ClassificationModel
import requests
from requests.auth import HTTPBasicAuth
import pandas as pd

flow_dict = {}
flow_predicted = {}
pkt_arr = []
predictions = 0
count = 0



def main():
    print("Starting")
    print('\n-------------\nmaking meter adjustments')
    headers = {'Accept': 'application/json'}
    meter_url = 'http://127.0.0.1:8181/onos/v1/devices'
    f = open('meter_calls.txt', 'w')
    start_time_meter = time.time()
    rsp = requests.get(headers=headers, url=meter_url, auth=HTTPBasicAuth('onos', 'rocks'))
    end_time_meter = time.time()
    total_meter_time = end_time_meter - start_time_meter
    f.write("Get devices time" + str(total_meter_time))
    rsp_js = rsp.json()
    response = 201
    print()
    start_timer = time.time()
    for device in rsp_js['devices']:
        device_id = device['id']
        # print(device_id)
        rsp_code = make_meter_adjustment(device_id)
        if rsp_code != 201:
            response = rsp_code
    if response == 201:
        print("successfully made meter entries\n-------------")
        total_time = time.time() - start_timer
        f.write("Made Meter Adjustment time:" + str(total_time))
        f.close()
    else:
        print("could not make meter entries\n-------------")

    # src_mac = "00:00:00:00:11:18"
    # vlan = "None"
    # src_mac = src_mac.replace(':', '%3A')
    # url = 'http://127.0.0.1:8181/onos/v1/hosts/' + src_mac + '/' + vlan
    # headers = {'Accept': 'application/json'}
    # rsp = requests.get(headers=headers, url=url, auth=HTTPBasicAuth('onos', 'rocks'))
    # js = rsp.json()
    # switch_id = str(js["locations"][0]["elementId"])
    # print("success")
    # switch_id_url = switch_id.replace(':', '%3A')
    # url = 'http://127.0.0.1:8181/onos/v1/statistics/ports/'+switch_id_url
    # rsp = requests.get(headers=headers, url=url, auth=HTTPBasicAuth('onos', 'rocks'))
    # num_ports = len(rsp.json()['statistics'][0]['ports'])
    # print(str(num_ports))
    # make_flow_adjustment('streaming', "00:00:00:00:11:18", 'None')
    try:
        sniff(iface="s1-eth1", prn=pkt_callback, store=0, timeout=615)
    except Exception as e:
        print(e)
        time.sleep(10)

    time.sleep(10)


def pkt_callback(pkt):
    global count
    count += 1
    # print(count)
    global flow_dict
    global flow_predicted
    # print("Processing packet")
    # pkt.show()  # debug statement
    decimal_data = []
    protocol = ""
    key = ""
    src_mac = ''
    # print("called")
    start_time = time.time()
    try:
        if pkt.haslayer(IP) and pkt.haslayer(Raw) and not pkt.haslayer('TLS'):  # if there is a payload

            # print("payload")
            ip_src = pkt[IP].src
            ip_dst = pkt[IP].dst

            if pkt.haslayer(TCP):
                protocol = "TCP"
                sport = pkt[TCP].sport
                dport = pkt[TCP].dport
            elif pkt.haslayer(UDP):
                protocol = "UDP"
                sport = pkt[UDP].sport
                dport = pkt[UDP].dport
            else:
                return
            src_mac = pkt[Ether].src
            if ip_src[:3] == "10.":
                key = ip_src + ip_dst + protocol + str(sport) + str(dport)
            else:
                key = ip_dst + ip_src + protocol + str(dport) + str(sport)
            if key in flow_predicted:
                if flow_predicted[key]:
                    return
            hex_data = linehexdump(
                pkt[IP].payload, onlyhex=1, dump=True).split(" ")
            decimal_data = list(map(hex_to_dec, hex_data))
    except Exception as e:
        print(e)
        print("Error reading data with scapy")
    if decimal_data:
        # print("decimal data")
        # np_arr = np.array(decimal_data)
        if key in flow_dict:
            pkts = flow_dict[key]
            # print('previous time is', time_previous)
            if len(pkts) < 1:
                flow_dict[key].append(decimal_data)
            if len(pkts) == 1 and not flow_predicted[key]:
                # prediction = predict_flow(pkts, key)
                flow_predicted[key] = True
                # print(src_mac)
                options = ['BITTORRENT', 'MESSAGING', 'SOCIALMEDIA', 'STREAMING']
                rnd = random.randint(0, 3)
                print('making random flow adjustment')
                make_flow_adjustment(options[rnd], src_mac, 'None')
                # print('final total time is')

                return
        else:
            flow_dict[key] = [decimal_data]
            flow_predicted[key] = False


def hex_to_dec(hex_data):
    return str(int(hex_data, base=16))


def make_flow_adjustment(category, src_mac, vlan):
    start = time.time()
    print('making flow adjustment')
    app_id = '0x123'
    meter_id = 0
    headers = {'Accept': 'application/json'}
    url = 'http://127.0.0.1:8181/onos/v1/flows/application/' + app_id
    # curl -X DELETE --header 'Accept: application/json' ''
    # requests.delete(headers=headers, url=url, auth=HTTPBasicAuth('onos', 'rocks'))
    src_mac_url = src_mac.replace(':', '%3A')
    url = 'http://127.0.0.1:8181/onos/v1/hosts/' + src_mac_url + '/' + vlan
    rsp = requests.get(headers=headers, url=url, auth=HTTPBasicAuth('onos', 'rocks'))
    js = rsp.json()
    switch_id = str(js["locations"][0]["elementId"])  # return format like: of:0000000000000001
    print(category.upper())
    category = category.upper()
    if category == "BITTORRENT":
        meter_id = 1
    elif category == "MESSAGING":
        meter_id = 2
    elif category == "SOCIALMEDIA":
        meter_id = 3
    elif category == "STREAMING":
        meter_id = 4
    else:
        meter_id = 1
    switch_id_url = switch_id.replace(':', '%3A')
    url = 'http://127.0.0.1:8181/onos/v1/statistics/ports/' + switch_id_url
    rsp = requests.get(headers=headers, url=url, auth=HTTPBasicAuth('onos', 'rocks'))
    num_ports = len(rsp.json()['statistics'][0]['ports'])
    # print(str(num_ports))
    print("---------\nMaking flow rule adjustments for category: " + category)
    url = 'http://127.0.0.1:8181/onos/v1/flows?appId=' + app_id
    priority = 60000
    flow_rule = {
        "flows": [
            {
                "priority": priority,
                "timeout": 0,
                "isPermanent": 'true',
                "deviceId": switch_id,
                "treatment": {
                    "instructions": [
                        {
                            "type": "OUTPUT",
                            "port": "1"
                        },
                        {
                            "type": "METER",
                            "meterId": meter_id
                        }
                    ]
                },
                "selector": {
                    "criteria": [
                        {
                            "type": "ETH_SRC",
                            "mac": src_mac
                        }
                    ]
                }
            }
        ]
    }
    # print(flow_rule)
    # print(src_mac)
    # print(url)

    rsp = requests.post(url=url, json=flow_rule, auth=HTTPBasicAuth('onos', 'rocks'))
    total = time.time() - start
    file = open('flow_adjustment_time.txt', 'a')
    file.write(str(total) + '\n')
    print(str(total))
    print(rsp.status_code)


def make_meter_adjustment(switch_id):
    rates = [13, 63, 125, 250]  # 0.104 0.504 1 2
    for rate in rates:
        meter = {
            "deviceId": switch_id,
            "unit": "KB_PER_SEC",
            "burst": "false",
            "bands": [
                {
                    "type": "DROP",
                    "rate": str(rate),
                    "burstSize": "0",
                    "prec": "0"
                }
            ]
        }
        meter_url = 'http://127.0.0.1:8181/onos/v1/meters/of%3A' + switch_id.split('of:')[1]
        rsp = requests.post(url=meter_url, json=meter, auth=HTTPBasicAuth('onos', 'rocks'))
    return rsp.status_code


if __name__ == '__main__':
    main()
