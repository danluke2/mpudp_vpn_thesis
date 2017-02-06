#!/bin/bash

#Purpose: start up the VPN connection to the server and capture one download to verify proper operation


tcpdump -i any -w $1_Init.pcap&

nohup openvpn --config /etc/openvpn/client.ovpn&

sleep 15

wget -q http://10.8.3.3/test/test16.txt -O /dev/null;

sleep 5

pkill tcpdump

