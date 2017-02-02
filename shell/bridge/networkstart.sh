#!/bin/bash

#sets up the required bridges for testing
#depending on the interfaces used (i.e. physical, usb ethernet, etc.), may need to adjust
#script to ensure speeds are set properly and bridges are set up correctly
#sleep timers inserted to allow interfaces to be recongnized prior to configuring bridges

#bridges need an IP address to allow SSH connections and starting/stopping TCP dumps


sleep 10

ifconfig eth2 0.0.0.0 up
ifconfig eth3 0.0.0.0 up
brctl addbr br0
brctl addif br0 eth2
brctl addif br0 eth3
ifconfig br0 up
ifconfig br0 10.8.2.220 netmask 255.255.255.0

sleep 10

ifconfig eth9 0.0.0.0 up
ifconfig eth10 0.0.0.0 up
brctl addbr br1
brctl addif br1 eth9
brctl addif br1 eth10
ifconfig br1 up
ifconfig br1 10.8.1.110 netmask 255.255.255.0


ethtool -s eth2 speed 10 duplex full autoneg on
ethtool -s eth3 speed 10 duplex full autoneg on
ethtool -s eth9 speed 10 duplex full autoneg on
ethtool -s eth10 speed 10 duplex full autoneg on
