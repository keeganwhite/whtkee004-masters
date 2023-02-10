#!/bin/bash

if [ -f .env ]
then
  export $(grep -v '^#' .env | xargs -d '\n')
fi

mkdir $OUTPUT_DIR # create flows directory
echo

num_files=`ls $RAW_PCAP_FILES | wc -l | tr -d '[:space:]'` # for keeping track of progress
i=1
for f in $RAW_PCAP_FILES
do
     echo "Processing $f ($i/$num_files)"
     ((i=i+1))
     ../../pkt2flow/pkt2flow -u -o $OUTPUT_DIR $f
     echo "File $f processed"
     echo
done
sudo chmod -R 777 $OUTPUT_DIR

echo "Finished splitting packets into flows"