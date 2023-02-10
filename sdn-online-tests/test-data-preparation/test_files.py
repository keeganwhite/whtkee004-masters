import csv
import os


def main():
    FLOW_FOLDER ="./flows/"
    APPLICATIONS=["WhatsAppFiles", "Instagram", "WhatsApp", "Messenger", "BitTorrent", "TikTok", "YouTube", "Facebook"]
    application_count = {}
    with open('./labels.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                application = row[1]
                file_path_arr = row[0].split("/")
                sub_folder = file_path_arr[0] + "/"
                file_path = FLOW_FOLDER + row[0]
                num_packets = row[2]
                if application in APPLICATIONS and int(num_packets) >= 15:
                    print("Trying to rename:" + file_path)
                    if application in application_count:
                        application_count[application] = application_count[application]+1
                    else:
                        application_count[application] = 1
                    file_path_new = FLOW_FOLDER + sub_folder + application + str(application_count[application]) + ".pcap"
                    if os.path.exists(file_path):
                        os.rename(file_path, file_path_new)
                        print("renamed: " + file_path + " to: " + file_path_new)
                else:
                    if os.path.exists(file_path):
                        # remove files that aren't needed to free space
                        os.remove(file_path)
                line_count += 1
        print(f'Processed {line_count} lines.')


if __name__ == '__main__':
    main()
