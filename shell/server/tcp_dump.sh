#!/bin/bash

#Purpose: start tcpdump capturing on all interfaces with size of 150 to limit PCAP size
#Note: may need to adjust to capture specific interface(s) depending on test running
#Note: could make “any” a shell variable to allow changing easily 


tcpdump -i any -s 150 -w $1_any.pcap&


