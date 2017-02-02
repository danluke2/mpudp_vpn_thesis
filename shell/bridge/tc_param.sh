#!/bin/bash

#set loss and delay on specified interface
# $1 is add, change, del
# $2 is interface id (ex: eth0)
# $3 is packet delay (ex: 5ms)
# $4 is loss rate (ex: 1%)

echo Setting Loss and Delay on interface

tc qdisc $1 dev $2 root netem delay $3 loss $4




