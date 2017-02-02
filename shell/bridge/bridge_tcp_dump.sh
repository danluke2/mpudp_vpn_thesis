#!/bin/bash

#start tcpdump on each bridge and capture first 150 Bytes to keep PCAP size smaller
#may want to adjust size to ensure all data is encrypted over tunnel for familiarization testing


nohup tcpdump -s 150 -i br1 -w $1_Bridge_br1.pcap &>/dev/null & sleep 5


nohup tcpdump -s 150 -i br0 -w $1_Bridge_br0.pcap &>/dev/null & sleep 5
