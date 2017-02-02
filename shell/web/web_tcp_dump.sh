#!/bin/bash

#start tcpdump and capture the first 150 bytes to minimize PCAP size


nohup tcpdump -s 150 -i eth4 -w $1_Web_eth4.pcap &>/dev/null & sleep 5


