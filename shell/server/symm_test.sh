#!/bin/bash


#Parameters:
#1 is test type: fullmesh, ndiffports, etc.
#2 is packet loss rate



#Bridge: ensure tc is set up prior to conducting tests
sshpass -p "mptcp11" ssh -p 22 root@10.8.1.110 "/home/bridge0/Documents/tc_param.sh add eth2 0ms $2; /home/bridge0/Documents/tc_param.sh add eth3 0ms $2; /home/bridge0/Documents/tc_param.sh add eth9 0ms $2; /home/bridge0/Documents/tc_param.sh add eth10 0ms $2; /home/bridge0/Documents/tc_qdisc.sh 0ms $1; exit"



#$1 test with $2 loss*******************************************************************************
echo $1 Test Starting with $2 Loss >> /home/vpnserver/Documents/log/status_$1


cd /home/vpnserver/Documents/run/$2/


#print tc status for reference 
sshpass -p "mptcp11" ssh -p 22 root@10.8.1.110 "cd /home/bridge0/Documents/$2/; /home/bridge0/Documents/tc_qdisc.sh 0ms $1; exit" 


#start tcpdump on each interface
/home/vpnserver/Documents/tcp_dump.sh $1

sleep 2


#uncomment if you want to capture traffic for ensuring traffic encrypted
#sshpass -p "mptcp11" ssh -p 22 root@10.8.1.110 "/home/bridg0/Documents/bridge_tcp_dump.sh $1; exit" 


#start tcpdumps on Web, ensure no_metrics_save set on web server
sshpass -p "mptcp11" ssh -p 22 root@10.8.3.3 "sysctl -w net.ipv4.tcp_no_metrics_save=1; cd /home/web/Documents/run/$2/; /home/web/Documents/web_tcp_dump.sh $1; exit" 

sleep 5


#start loop to run tests for all delays
#note: RTT is double the dalay
for delay in 0ms 0.5ms 5ms 10ms 20ms 30ms 40ms 50ms
   do


   echo **********$delay************** >> /home/vpnserver/Documents/log/status_$1


   #Bridge: make changes to delay rate
   sshpass -p "mptcp11" ssh -p 22 root@10.8.1.110 "/home/bridge0/Documents/tc_param.sh change eth2 $delay $2; /home/bridge0/Documents/tc_param.sh change eth3 $delay $2; /home/bridge0/Documents/tc_param.sh change eth9 $delay $2; /home/bridge0/Documents/tc_param.sh change eth10 $delay $2; /home/bridge0/Documents/tc_qdisc.sh $delay $1; exit"


   #ping test parameters to verify loss rate 
   #Note: this can be commented out once you are comfortable that delay/loss rates are as expected
   ping -c 2000 -f 10.8.1.1 >> ping.txt
   cat ping.txt | grep "10.8\|2000\|rtt" >> /home/vpnserver/Documents/log/status_$1
   rm ping.txt

   ping -c 2000 -f 10.8.2.2 >> ping.txt
   cat ping.txt | grep "10.8\|2000\|rtt" >> /home/vpnserver/Documents/log/status_$1
   rm ping.txt


   #perform downloads on Client
   sshpass -p "mptcp11" ssh -p 22 root@10.8.2.2 "/home/client/Documents/downloads.sh; wait; exit"

done



sshpass -p "mptcp11" ssh -p 22 root@10.8.1.110 "/home/bridge0/Documents/tc_param.sh del eth2 50ms $2; /home/bridge0/Documents/tc_param.sh del eth3 50ms $2; /home/bridge0/Documents/tc_param.sh del eth9 50ms $2; /home/bridge0/Documents/tc_param.sh del eth10 50ms $2; kill tcpdump; exit"



#kill local tcpdump
pkill tcpdump

sleep 10

#kill tcpdump on web and run t-shark analysis
sshpass -p "mptcp11" ssh -p 22 root@10.8.3.3 "pkill tcpdump; sleep 1; cd /home/web/Documents/run/$2/; tshark -r $1_Web_eth4.pcap -q -z conv,tcp > $1.csv; wait; exit"



