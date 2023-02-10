import glob
import os
import shutil
import csv


def main():
    folder = '/home/kwhite/Desktop/flows/'
    unused_tcp = '/home/kwhite/Desktop/flows/unused/tcp_syn/'
    used_tcp = '/home/kwhite/Desktop/expermental/final-test-data/tcp_syn/'
    tcp_folder = '/home/kwhite/Desktop/expermental/tcp_syn/'
    unused_udp = '/home/kwhite/Desktop/flows/unused/udp/'
    used_udp = '/home/kwhite/Desktop/expermental/final-test-data/udp/'
    udp_folder = '/home/kwhite/Desktop/expermental/udp/'
    count = 0
    with open("experimental-corrected.csv", "r") as input:
        for line in input:
            line_arr = line.split(',')
            if count == 0:
                count += 1
                continue
            elif 'tcp_syn' in line:
                fname = line_arr[0]
                fname = fname.split('/')[1]
                # print(tcp_folder + fname)
                if os.path.isfile(tcp_folder + fname):
                    count+=1
                    shutil.move(tcp_folder + fname, used_tcp + fname)
            elif 'udp' in line:
                fname = line_arr[0]
                fname = fname.split('/')[1]
                if os.path.isfile(udp_folder + fname):
                    shutil.move(udp_folder + fname, used_udp + fname)
                    count += 1
            if count % 100000 == 0:
                print(count)


if __name__ == '__main__':
    main()
