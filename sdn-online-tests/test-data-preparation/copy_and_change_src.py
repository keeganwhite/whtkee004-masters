import os
import shutil

from scapy.layers.l2 import Ether
from scapy.utils import PcapReader, wrpcap


def main():
    rootdir = '/home/kwhite/Desktop/expermental/experiment'
    applications = {"Instagram": 0, "WhatsApp": 0, "Messenger": 0, "BitTorrent": 0, "TikTok": 0, "YouTube": 0,
                    "Facebook": 0}
    new_dir = '/home/kwhite/Desktop/expermental/combined/'
    count = 0
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            valid = is_valid(subdir + '/' + file)
            if count % 10 == 0 and count != 0:
                print(count)
            if valid:
                count += 1
                name = ''.join([i for i in file if not i.isdigit()])
                if 'Instagram' in name:
                    if applications['Instagram'] < 50:
                        new_sub_dir = new_dir + '00:00:00:00:11:11/'
                        try:
                            os.mkdir(new_sub_dir)
                            shutil.copy(subdir + '/' + file, new_sub_dir)
                            applications['Instagram'] += 1
                        except FileExistsError as e:
                            shutil.copy(subdir + '/' + file, new_sub_dir)
                            applications['Instagram'] += 1
                        pcap = PcapReader(new_sub_dir + file)
                        final_data = []
                        for pkt in pcap:
                            pkt[Ether].src = "00:00:00:00:11:11"
                            final_data.append(pkt)
                        wrpcap(new_sub_dir + file, final_data)
                    elif applications['Instagram'] < 100:
                        new_sub_dir = new_dir + '00:00:00:00:11:12/'
                        try:
                            os.mkdir(new_sub_dir)
                            shutil.copy(subdir + '/' + file, new_sub_dir)
                            applications['Instagram'] += 1
                        except FileExistsError:
                            shutil.copy(subdir + '/' + file, new_sub_dir)
                            applications['Instagram'] += 1
                        pcap = PcapReader(new_sub_dir + file)
                        final_data = []
                        for pkt in pcap:
                            pkt[Ether].src = "00:00:00:00:11:12"
                            final_data.append(pkt)
                        wrpcap(new_sub_dir + file, final_data)
                if 'WhatsApp' in name and 'WhatsAppFiles' not in name:
                    if applications['WhatsApp'] < 50:
                        new_sub_dir = new_dir + '00:00:00:00:11:13/'
                        try:
                            os.mkdir(new_sub_dir)
                            shutil.copy(subdir + '/' + file, new_sub_dir)
                            applications['WhatsApp'] += 1
                        except FileExistsError as e:
                            shutil.copy(subdir + '/' + file, new_sub_dir)
                            applications['WhatsApp'] += 1
                        pcap = PcapReader(new_sub_dir + file)
                        final_data = []
                        for pkt in pcap:
                            pkt[Ether].src = "00:00:00:00:11:13"
                            final_data.append(pkt)
                        wrpcap(new_sub_dir + file, final_data)
                    elif applications['WhatsApp'] < 100:
                        new_sub_dir = new_dir + '00:00:00:00:11:14/'
                        try:
                            os.mkdir(new_sub_dir)
                            shutil.copy(subdir + '/' + file, new_sub_dir)
                            applications['WhatsApp'] += 1
                        except FileExistsError:
                            shutil.copy(subdir + '/' + file, new_sub_dir)
                            applications['WhatsApp'] += 1
                        pcap = PcapReader(new_sub_dir + file)
                        final_data = []
                        for pkt in pcap:
                            pkt[Ether].src = "00:00:00:00:11:14"
                            final_data.append(pkt)
                        wrpcap(new_sub_dir + file, final_data)

                # Messenger
                if 'Messenger' in name:
                    if applications['Messenger'] < 50:
                        new_sub_dir = new_dir + '00:00:00:00:11:15/'
                        try:
                            os.mkdir(new_sub_dir)
                            shutil.copy(subdir + '/' + file, new_sub_dir)
                            applications['Messenger'] += 1
                        except FileExistsError as e:
                            shutil.copy(subdir + '/' + file, new_sub_dir)
                            applications['Messenger'] += 1
                        pcap = PcapReader(new_sub_dir + file)
                        final_data = []
                        for pkt in pcap:
                            pkt[Ether].src = "00:00:00:00:11:15"
                            final_data.append(pkt)
                        wrpcap(new_sub_dir + file, final_data)
                    elif applications['Messenger'] < 100:
                        new_sub_dir = new_dir + '00:00:00:00:11:16/'
                        try:
                            os.mkdir(new_sub_dir)
                            shutil.copy(subdir + '/' + file, new_sub_dir)
                            applications['Messenger'] += 1
                        except FileExistsError:
                            shutil.copy(subdir + '/' + file, new_sub_dir)
                            applications['Messenger'] += 1
                        pcap = PcapReader(new_sub_dir + file)
                        final_data = []
                        for pkt in pcap:
                            pkt[Ether].src = "00:00:00:00:11:16"
                            final_data.append(pkt)
                        wrpcap(new_sub_dir + file, final_data)

                # BitTorrent
                if 'BitTorrent' in name:
                    if applications['BitTorrent'] < 50:
                        new_sub_dir = new_dir + '00:00:00:00:11:17/'
                        try:
                            os.mkdir(new_sub_dir)
                            shutil.copy(subdir + '/' + file, new_sub_dir)
                            applications['BitTorrent'] += 1
                        except FileExistsError as e:
                            shutil.copy(subdir + '/' + file, new_sub_dir)
                            applications['BitTorrent'] += 1
                        pcap = PcapReader(new_sub_dir + file)
                        final_data = []
                        for pkt in pcap:
                            pkt[Ether].src = "00:00:00:00:11:17"
                            final_data.append(pkt)
                        wrpcap(new_sub_dir + file, final_data)
                    elif applications['BitTorrent'] < 100:
                        new_sub_dir = new_dir + '00:00:00:00:11:18/'
                        try:
                            os.mkdir(new_sub_dir)
                            shutil.copy(subdir + '/' + file, new_sub_dir)
                            applications['BitTorrent'] += 1
                        except FileExistsError:
                            shutil.copy(subdir + '/' + file, new_sub_dir)
                            applications['BitTorrent'] += 1
                        pcap = PcapReader(new_sub_dir + file)
                        final_data = []
                        for pkt in pcap:
                            pkt[Ether].src = "00:00:00:00:11:18"
                            final_data.append(pkt)
                        wrpcap(new_sub_dir + file, final_data)

                # TikTok
                if 'TikTok' in name:
                    if applications['TikTok'] < 50:
                        new_sub_dir = new_dir + '00:00:00:00:11:19/'
                        try:
                            os.mkdir(new_sub_dir)
                            shutil.copy(subdir + '/' + file, new_sub_dir)
                            applications['TikTok'] += 1
                        except FileExistsError as e:
                            shutil.copy(subdir + '/' + file, new_sub_dir)
                            applications['TikTok'] += 1
                        pcap = PcapReader(new_sub_dir + file)
                        final_data = []
                        for pkt in pcap:
                            pkt[Ether].src = "00:00:00:00:11:19"
                            final_data.append(pkt)
                        wrpcap(new_sub_dir + file, final_data)
                    elif applications['TikTok'] < 100:
                        new_sub_dir = new_dir + '00:00:00:00:11:20/'
                        try:
                            os.mkdir(new_sub_dir)
                            shutil.copy(subdir + '/' + file, new_sub_dir)
                            applications['TikTok'] += 1
                        except FileExistsError:
                            shutil.copy(subdir + '/' + file, new_sub_dir)
                            applications['TikTok'] += 1
                        pcap = PcapReader(new_sub_dir + file)
                        final_data = []
                        for pkt in pcap:
                            pkt[Ether].src = "00:00:00:00:11:20"
                            final_data.append(pkt)
                        wrpcap(new_sub_dir + file, final_data)

                # YouTube
                if 'YouTube' in name:
                    if applications['YouTube'] < 50:
                        new_sub_dir = new_dir + '00:00:00:00:11:21/'
                        try:
                            os.mkdir(new_sub_dir)
                            shutil.copy(subdir + '/' + file, new_sub_dir)
                            applications['YouTube'] += 1
                        except FileExistsError as e:
                            shutil.copy(subdir + '/' + file, new_sub_dir)
                            applications['YouTube'] += 1
                        pcap = PcapReader(new_sub_dir + file)
                        final_data = []
                        for pkt in pcap:
                            pkt[Ether].src = "00:00:00:00:11:21"
                            final_data.append(pkt)
                        wrpcap(new_sub_dir + file, final_data)
                    elif applications['YouTube'] < 100:
                        new_sub_dir = new_dir + '00:00:00:00:11:22/'
                        try:
                            os.mkdir(new_sub_dir)
                            shutil.copy(subdir + '/' + file, new_sub_dir)
                            applications['YouTube'] += 1
                        except FileExistsError:
                            shutil.copy(subdir + '/' + file, new_sub_dir)
                            applications['YouTube'] += 1
                        pcap = PcapReader(new_sub_dir + file)
                        final_data = []
                        for pkt in pcap:
                            pkt[Ether].src = "00:00:00:00:11:22"
                            final_data.append(pkt)
                        wrpcap(new_sub_dir + file, final_data)

                # Facebook
                if 'Facebook' in name:
                    if applications['Facebook'] < 50:
                        new_sub_dir = new_dir + '00:00:00:00:11:23/'
                        try:
                            os.mkdir(new_sub_dir)
                            shutil.copy(subdir + '/' + file, new_sub_dir)
                            applications['Facebook'] += 1
                        except FileExistsError as e:
                            shutil.copy(subdir + '/' + file, new_sub_dir)
                            applications['Facebook'] += 1
                        pcap = PcapReader(new_sub_dir + file)
                        final_data = []
                        for pkt in pcap:
                            pkt[Ether].src = "00:00:00:00:11:23"
                            final_data.append(pkt)
                        wrpcap(new_sub_dir + file, final_data)
                    elif applications['Facebook'] < 100:
                        new_sub_dir = new_dir + '00:00:00:00:11:24/'
                        try:
                            os.mkdir(new_sub_dir)
                            shutil.copy(subdir + '/' + file, new_sub_dir)
                            applications['Facebook'] += 1
                        except FileExistsError:
                            shutil.copy(subdir + '/' + file, new_sub_dir)
                            applications['Facebook'] += 1
                        pcap = PcapReader(new_sub_dir + file)
                        final_data = []
                        for pkt in pcap:
                            pkt[Ether].src = "00:00:00:00:11:24"
                            final_data.append(pkt)
                        wrpcap(new_sub_dir + file, final_data)


def is_valid(file):
    if os.path.exists(file):
        # print(payload_source)
        pcap = PcapReader(file)
        packets = []
        num_usable_packets = 0
        try:
            for pkt in pcap:
                if pkt.haslayer('Raw') and not pkt.haslayer('TLS'):
                    num_usable_packets += 1
                packets.append(pkt)
            # print(num_usable_packets)
            if num_usable_packets >= 30:
                # print("writing pcap", file)
                wrpcap(file, packets)
                return True
            else:
                return False
        except:
            print()
    else:
        return False
    return True


if __name__ == '__main__':
    main()
