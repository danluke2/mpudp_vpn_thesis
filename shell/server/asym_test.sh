#!/bin/bash


#Parameters:
#$1 is primary link delay (includes ms)
#$2 is sec link delay (includes ms)
#$3 is pri link loss
#$4 is sec link loss
#$5 is folder label




#test with $1, $2 delays and $3,$4 loss*******************************************************************************
echo Test Starting with $1 and $2 Delays $3 and $4 Loss >> /home/vpnserver/Documents/log/status_asym



#Bridge: make changes to delay rate
sshpass -p "mptcp11" ssh -p 22 root@10.8.1.110 "/home/bridge0/Documents/tc_param.sh change eth2 $2 $4; /home/bridge0/Documents/tc_param.sh change eth3 $2 $4; /home/bridge0/Documents/tc_param.sh change eth9 $1 $3; /home/bridge0/Documents/tc_param.sh change eth10 $1 $3; /home/bridge0/Documents/tc_qdisc.sh $1 $3; exit"


cd /home/vpnserver/Documents/test/$5/
#start tcpdump on each interface
tcpdump -i any -s 150 -w $1_$delay_any_$i.pcap&


sleep 2


#start tcpdumps on Web
sshpass -p "mptcp11" ssh -p 22 root@10.8.3.3 "cd /home/web/Documents/test/$5/; /home/web/Documents/web_tcp_dump.sh asym; exit"


#perform downloads on Client
sshpass -p "mptcp11" ssh -p 22 root@10.8.2.2 "/home/client/Documents/download.sh; exit"



sleep 2


#kill local tcpdump
pkill tcpdump


sleep 2

#kill tcpdump on web and run t-shark analysis
sshpass -p "mptcp11" ssh -p 22 root@10.8.3.3 "pkill tcpdump; sleep 2; cd /home/web/Documents/test/$5/; tshark -r asym_Web_eth4.pcap -q -z conv,tcp > $5.csv; wait; exit"



