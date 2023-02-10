# logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from itertools import count

import requests
from requests.auth import HTTPBasicAuth
from scapy.all import sendp, IP, UDP, Ether, TCP, rdpcap
from scapy.all import *
from scapy.sendrecv import sendpfast
import os
import csv
import sys
import shutil


def main():
    # ______ USED TO SEND
    # ****************************************************************************************
    mac_address = sys.argv[1]
    host_number = str(sys.argv[2])
    directory = "/path/to/pcaps/" + str(mac_address) + '/'
    csv_sent = str(mac_address) + ".csv"
    interface_name = "h" + host_number + "-eth1"
    if mac_address == '00:00:00:00:11:10':
        interface_name = 'i1-eth1'
        directory = "/path/to/pcaps/" + str(sys.argv[3]) + '/'
    start_time_outer = time.time()
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        arr = send_pcap(f, interface_name)
        print(arr)
        key = arr[0]
        time_elapsed = arr[1]
        try:
            with open(mac_address + "_sent_key.csv", 'a') as file:
                writer = csv.writer(file)
                filename_arr = filename.split(".")
                label = filename_arr[0]
                label = ''.join([i for i in label if not i.isdigit()])
                print(label)
                writer.writerow([label, key])
        except Exception as e:
            print(e)
        end_time = time.time()
        if end_time - start_time_outer >= 600:
            break

def get_bytes_sent(port):
    headers = {'Accept': 'application/json'}
    meter_url = 'http://127.0.0.1:8181/onos/v1/statistics/ports'
    rsp = requests.get(headers=headers, url=meter_url, auth=HTTPBasicAuth('onos', 'rocks'))
    rsp_js = rsp.json()
    bytes_received = rsp_js['statistics'][0]['ports'][port]['bytesReceived']
    print(bytes_received)
    return int(bytes_received)


def send_pcap(file_name, interface_name):
    """
    Sends PCAP file
    :param interface_name: interface to send via
    :param file_name: pcap tp send
    :return: array of key value generated from sending and the time taken to send
    """
    inethi_sample = rdpcap(file_name)
    for pkt in inethi_sample:
        if pkt.haslayer(IP) and pkt.haslayer(Raw) and not pkt.haslayer('TLS'):
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

            if ip_src[:3] == "10.":
                key = ip_src + ip_dst + protocol + str(sport) + str(dport)
                break
            else:
                key = ip_dst + ip_src + protocol + str(dport) + str(sport)
                break
    try:
        start_time = time.time()
        sendpfast(inethi_sample, iface=interface_name, mbps=2)
        end_time = time.time()
        time_elapsed = end_time - start_time
        return [key, time_elapsed]
    except Exception as e:
        print(e)


def create_folders(num_hosts):
    """
    Divides the pcap files available evenly into folders
    """

    count = 0
    directory_num = 1
    directory = "./path/to/pcaps"
    number_files = len([name for name in os.listdir(directory) if os.path.isfile(os.path.join(directory, name))])
    print(number_files)
    files_per_host = int(number_files / num_hosts)
    print(files_per_host)
    for i in range(num_hosts):
        try:
            os.mkdir(os.path.join(directory, str(i + 1) + "/"))
        except:
            print("Folder exists")
    for filename in os.listdir(directory):
        if filename.endswith(".pcap"):
            f = os.path.join(directory, filename)
            shutil.copy2(f, (os.path.join(directory, str(directory_num) + "/")))
            count += 1
        if count == files_per_host:
            directory_num += 1
            count = 0


def generate_packets(src_mac, payload_source, filename):
    """
    Pre-generates PCAP files in the correct format.
    :param payload_source: pcap file
    :param filename: name of output
    :return: bool value indicating success or failiure
    """
    inethi_sample = rdpcap(payload_source)

    counter = 0
    # print("Getting payloads from iNethi data")
    sample_data = []
    flow_info = []
    num_usable_packets = 0
    udp = False
    final_data = []
    count = 0
    for pkt in inethi_sample:
        if pkt.haslayer(Ether) and pkt.haslayer(IP) and pkt.haslayer(Raw) and not pkt.haslayer('TLS'):
            pkt[Ether].src = src_mac
            pkt[Ether].dst = "00:00:00:00:11:10"  # 'internet' MAC address
            count += 1
        elif pkt.haslayer(Ether):
            pkt[Ether].src = src_mac
            pkt[Ether].dst = "00:00:00:00:11:10"  # 'internet' MAC address
    if count >= 10:
        wrpcap("/path/to/destination/" + str(src_mac) + '/' + filename, inethi_sample)
        return True
    else:
        return False


if __name__ == "__main__":
    main()
