#!/bin/bash

#Purpose: echo to status file the current settings on each interface to allow debugging

echo ***** START ***** $1 ***** >> /home/bridge0/Documents/log/status_$2

echo ETH2 Qdisc >> /home/bridge0/Documents/log/status_$2
tc qdisc show dev eth2 >> /home/bridge0/Documents/log/status_$2

echo ETH3 Qdisc >> /home/bridge0/Documents/log/status_$2
tc qdisc show dev eth3 >> /home/bridge0/Documents/log/status_$2

echo ETH9 Qdisc >> /home/bridge0/Documents/log/status_$2
tc qdisc show dev eth9 >> /home/bridge0/Documents/log/status_$2

echo ETH10 Qdisc >> /home/bridge0/Documents/log/status_$2
tc qdisc show dev eth10 >> /home/bridge0/Documents/log/status_$2

echo  ***** $1 ***** FINISH ***** >> /home/bridge0/Documents/log/status_$2

echo >> /home/bridge0/Documents/log/status_$2


