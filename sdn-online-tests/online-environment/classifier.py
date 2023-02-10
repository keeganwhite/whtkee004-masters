import csv
import time

from scapy.all import *
from classification_model import ClassificationModel
import requests
from requests.auth import HTTPBasicAuth
import pandas as pd

flow_dict = {}
flow_predicted = {}
pkt_arr = []
model = ClassificationModel("path/to/model")
predictions = 0
count = 0
transformation_time = {}


def main():
    global transformation_time
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

    try:
        sniff(iface="s2-eth1", prn=pkt_callback, store=0, timeout=615)
    except Exception as e:
        print(e)
        time.sleep(10)
    try:
        print(transformation_time)
        df = pd.DataFrame([transformation_time])
        print(df.head())
        df.to_csv("trans_time.csv")
    except Exception as e:
        print('error')
        print(e)
    time.sleep(10)


def predict_flow(packet_array, key):
    global model
    try:
        results = model.predict_flow(packet_array)
    except Exception as e:
        print(e)
        time.sleep(5)
    prediction = results[0]
    time_elapsed = results[1]
    print("The prediction is: ", prediction)
    with open('predictions.csv', 'a') as file:
        writer = csv.writer(file)
        writer.writerow([prediction, key])
    with open('time.csv', 'a') as file:
        writer = csv.writer(file)
        writer.writerow([time_elapsed])
    global predictions
    predictions += 1
    if predictions % 100 == 0:
        print("Made", predictions, "predictions")
    print('done predicting')
    return prediction



def pkt_callback(pkt):
    global count
    count += 1
    # print(count)
    global flow_dict
    global flow_predicted
    global transformation_time

    num_bytes = 144
    decimal_data = []
    protocol = ""
    key = ""
    src_mac = ''

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
            # fix length of payload
            if len(decimal_data) >= num_bytes:
                decimal_data = decimal_data[:num_bytes]
            elif len(decimal_data) < num_bytes:
                for i in range(len(decimal_data), num_bytes):
                    decimal_data.append(0)
            for i in range(20):
                decimal_data[i] = 0  # mask first 20 bytes
    except Exception as e:
        print(e)
        print("Error reading data with scapy")
    if decimal_data:
        if key in flow_dict:
            pkts = flow_dict[key]
            time_previous = transformation_time[key]

            if len(pkts) < 3:
                flow_dict[key].append(decimal_data)
            if len(pkts) == 3 and not flow_predicted[key]:

                prediction = predict_flow(pkts, key)
                flow_predicted[key] = True
                make_flow_adjustment(prediction, src_mac, 'None')
                transformation_time[key] = time.time() - time_previous
                return
        else:
            flow_dict[key] = [decimal_data]
            flow_predicted[key] = False
            transformation_time[key] = start_time


def hex_to_dec(hex_data):
    return str(int(hex_data, base=16))


def make_flow_adjustment(category, src_mac, vlan):
    start = time.time()
    print('making flow adjustment')
    app_id = '0x123'

    headers = {'Accept': 'application/json'}

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
    # switch_id_url = switch_id.replace(':', '%3A')
    # url = 'http://127.0.0.1:8181/onos/v1/statistics/ports/'+switch_id_url
    # rsp = requests.get(headers=headers, url=url, auth=HTTPBasicAuth('onos', 'rocks'))

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
    priority = 60000
    # switches = []
    # url = 'http://127.0.0.1:8181/onos/v1/devices'
    # headers = {'Accept': 'application/json'}
    # rsp = requests.get(headers=headers, url=url, auth=HTTPBasicAuth('onos', 'rocks'))
    # rsp_js = rsp.json()
    # devices = rsp_js['devices']
    #
    # for device in devices:
    #     switches.append(device['id'])
    # url = 'http://127.0.0.1:8181/onos/v1/flows?appId=' + app_id
    # for switch in switches:
    #     print(switch_id)
    #     flow_rule = {
    #             "flows": [
    #                 {
    #                     "priority": priority,
    #                     "timeout": 0,
    #                     "isPermanent": 'true',
    #                     "deviceId": switch,
    #                     "treatment": {
    #                         "instructions": [
    #                             {
    #                                 "type": "OUTPUT",
    #                                 "port": "1"
    #                             },
    #                             {
    #                                 "type": "METER",
    #                                 "meterId": meter_id
    #                             }
    #                         ]
    #                     },
    #                     "selector": {
    #                         "criteria": [
    #                             {
    #                                 "type": "ETH_SRC",
    #                                 "mac": src_mac
    #                             }
    #                         ]
    #                     }
    #                 }
    #             ]
    #         }
    #
    #     rsp = requests.post(url=url, json=flow_rule, auth=HTTPBasicAuth('onos', 'rocks'))
    #     print(rsp)
    rsp = requests.post(url=url, json=flow_rule, auth=HTTPBasicAuth('onos', 'rocks'))
    print(rsp.status_code)
    # total = time.time() - start
    # file = open('flow_adjustment_time.txt', 'a')
    # file.write(str(total)+'\n')
    # print(str(total))



def make_meter_adjustment(switch_id):
    rates = [100, 200, 200, 1000]  # in kilobits
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

