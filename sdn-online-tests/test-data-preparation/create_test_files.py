import csv
import os
from scapy.all import *
import shutil


def main():
    flow_folder = "/path/to/flows/folder/"
    applications = ["Instagram", "WhatsApp", "Messenger", "BitTorrent", "TikTok", "YouTube",
                    "Facebook"]
    label_file = '/home/kwhite/Desktop/expermental/experimental.csv'
    new_folder = "/path/to/output/folder/"
    renamed = rename_pcap_files(label_file, flow_folder, applications, new_folder)
    if renamed:
        print("files renamed successfully")
    else:
        print("files could not be renamed")


def rename_pcap_files(flow_location_file, flow_folder, applications, new_folder):
    """
    Rename all pcap files after the application it is labelled as
    :param flow_location_file: the csv file with the path to the flow files and labels for them
    :param flow_folder: the folder with the pcap flow files
    :param applications: the applications we want present in the final pcap files
    :return: true if the file names been changed else false
    """
    application_count = {}
    flows = []
    try:
        if os.path.exists(flow_location_file):
            with open(flow_location_file) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                line_count = 0
                for row in csv_reader:
                    if line_count == 0:
                        print(f'Column names are {", ".join(row)}')
                        line_count += 1
                    else:
                        application = row[2]
                        file_path_arr = row[1].split("/")
                        sub_folder = file_path_arr[3] + "/"
                        f = file_path_arr[4]
                        file_path = flow_folder + sub_folder + f
                        print(f'file_path is {file_path}')
                        flows.append(file_path)
                        # meets_requirements = delete_unusable_pcaps(file_path, 20)
                        meets_requirements = True
                        if application in applications and meets_requirements:
                            print("Trying to rename:" + file_path)
                            if application in application_count:
                                application_count[application] = application_count[application] + 1
                            else:
                                application_count[application] = 1
                            file_path_new = new_folder + sub_folder + application + str(
                                application_count[application]) + ".pcap"
                            if os.path.exists(file_path):
                                shutil.move(file_path, file_path_new)
                                print("renamed: " + file_path + " to: " + file_path_new)
                        # else:
                        #     if os.path.exists(file_path):
                        #         # remove files that aren't needed to free space
                        #         os.remove(file_path)
                    line_count += 1
                    # print(line_count)
                    # if line_count == 10:
                    #     break
                print(f'Processed {line_count} lines.')
                return True
    except Exception as e:
        print(e)
        return False


def delete_unusable_pcaps(payload_source, number_of_packets):
    """
    Checks if a pcap file has enough packet with IP v4 payloads s to be sent through the network
    :param payload_source: the pcap file
    :param number_of_packets: the number of packets required for the pcap to be viable
    :return: true or false
    """
    if os.path.exists(payload_source):
        # print(payload_source)
        pcap = PcapReader(payload_source)
        packets = []
        num_usable_packets = 0
        try:
            for pkt in pcap:
                if pkt.haslayer('IP') and pkt.haslayer('Raw'):
                    pkt = update_source_and_destination(['10.0.0.2'], ['10.0.0.1'], '10.0', pkt)
                    num_usable_packets += 1
                packets.append(pkt)
            if num_usable_packets >= number_of_packets:
                print("writing pcap", payload_source)
                wrpcap(payload_source, packets)
                return True
            else:
                if os.path.exists(payload_source):
                    # remove files that aren't needed to free space
                    os.remove(payload_source)
                return False
        except:
            print()
    else:
        return False


def update_source_and_destination(sources, destinations, prefix, pkt):
    """
    Changes source and destination IP addresses of packet from pcap file if there is an IP v4 layer
    :param sources: list of IP sources
    :param destinations: list of IP destinations
    :param prefix: the local IP address prefix, i.e. 192/10. etc.
    :param pkt: the packet extracted from the pcap
    :return: edited packet with new source and destination
    """
    ip_layer = pkt.getlayer("IP")
    if ip_layer is None:
        return pkt
    src = ip_layer.src
    dst = ip_layer.dst
    if src[:3] == prefix:
        ip_layer.src = sources[0]
        ip_layer.dst = destinations[0]  # destination will be the server
        return pkt
    elif dst[:3] == prefix:
        ip_layer.src = sources[0]  # src will be the server
        ip_layer.dst = destinations[0]
        return pkt


if __name__ == '__main__':
    main()
