import os
import glob
import time


def main():
    start_time = time.time()
    clean_flows_folders('./', './flows/')
    end_time = time.time()
    print('Total time to clean', str(end_time - start_time))


def clean_flows_folders(labels_files_folder, flow_directory):
    skip = True
    path = labels_files_folder + "*.csv"
    labelled_files = {}
    all_files = []
    tcp_directory = flow_directory + "tcp_syn/*.pcap"
    udp_directory = flow_directory + "udp/*.pcap"
    matches = 0
    for file in glob.glob(tcp_directory):
        all_files.append(file)
    for file in glob.glob(udp_directory):
        all_files.append(file)
    print("total TCP and UDP files:", str(len(all_files)))
    for fname in glob.glob(path):
        # print(fname)
        with open(fname) as f_read:
            for line in f_read:
                # print(line)
                if skip:  # skip header row
                    skip = False
                else:
                    split_line = line.strip().split(',')
                    # get the file path and label
                    file_path = split_line[0]
                    file_path = flow_directory + file_path
                    labelled_files[file_path] = 1
        skip = True
    print("There are a total of", str(len(labelled_files)), "labelled flows")
    for file in all_files:
        if file not in labelled_files:
            if os.path.exists(file):
                # remove files that aren't needed to free space
                os.remove(file)
                matches += 1
    print("There are a total of", str(len(all_files)), "flows")
    print("There are a total of", str(matches), "flow files deleted")


if __name__ == '__main__':
    main()
