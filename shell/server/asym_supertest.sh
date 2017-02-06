#!/bin/bash

#Settings:
#set desired mem parameters before test
#ensure iptables set for server and client

#Parameters:
#$1=congestion control
#$2=20 or 40ms
#$3=10 or 20ms
#$4=8 or 15ms
#$5=12 or 25ms
#$6=5ms or 10ms
#$7= 15 or 30ms



#log openvpn files
#we don't want to cache info on tcp sessions since we are running repeated tests

cd /home/vpnserver/Documents/log/
sudo cp /etc/openvpn/tcp443.conf .
sysctl -w net.ipv4.tcp_no_metrics_save=1

sshpass -p "mptcp11" ssh -p 22 root@10.8.2.2 "sysctl -w net.ipv4.tcp_no_metrics_save=1; cd /home/client/Documents/log/; cp /etc/openvpn/client.ovpn .; exit"



#set testing variables for client and then server

sysctl -w net.ipv4.tcp_congestion_control=$1
sshpass -p "mptcp11" ssh -p 22 root@10.8.2.2 "sysctl -w net.ipv4.tcp_no_metrics_save=1; sysctl -w net.ipv4.tcp_congestion_control=$1; cd /home/client/Documents/log/ ; echo MP Asym Parameters >> status_asym; sysctl -w net.mptcp.mptcp_enabled=1 >> status_asym; sysctl -w net.mptcp.mptcp_path_manager=fullmesh >> status_asym; sysctl net.ipv4.tcp_congestion_control >> status_asym; exit"


cd /home/vpnserver/Documents/log/
echo CS Parameters >> status_asym
sysctl -w net.mptcp.mptcp_enabled=1 >> status_asym
sysctl -w net.mptcp.mptcp_path_manager=fullmesh >>status_asym
sysctl net.ipv4.tcp_congestion_control >> status_asym
service openvpn restart


#start tcpdump, start openvpn connection, warmup download, kill tcpdump 
sshpass -p "mptcp11" ssh -p 22 root@10.8.2.2 "cd /home/client/Documents/log/ ; nohup /home/client/Documents/vpnstart.sh $test; exit"


cd /home/vpnserver/Documents/
mkdir test
chmod +777 test
cd test/
for dir in $2_0_even $2_P1_even $2_P5_even $2_1P_even $2_0_mod $2_P1_mod $2_P5_mod $2_1P_mod $2_0_sev $2_P1_sev $2_P5_sev $2_1P_sev
do
   mkdir $dir
   chmod +777 $dir
done
 
#create folders on web
sshpass -p "mptcp11" ssh -p 22 root@10.8.3.3 "cd /home/web/Documents/;./directory_asym.sh $2 exit"



#Bridge: set up tc for tests
sshpass -p "mptcp11" ssh -p 22 root@10.8.1.110 "/home/bridge0/Documents/tc_param.sh add eth2 0ms 0%; /home/bridge0/Documents/tc_param.sh add eth3 0ms 0%; /home/bridge0/Documents/tc_param.sh add eth9 0ms 0%; /home/bridge0/Documents/tc_param.sh add eth10 0ms 0%; /home/bridge0/Documents/tc_qdisc.sh 0ms 0%; exit"




 #run various tests and repeat
   /home/vpnserver/Documents/asym_test.sh  $3 $3 0% 0% $2_0_even
   /home/vpnserver/Documents/asym_test.sh  $3 $3 0.05% 0.05% $2_P1_even
   /home/vpnserver/Documents/asym_test.sh  $3 $3 0.25% 0.25% $2_P5_even
   /home/vpnserver/Documents/asym_test.sh  $3 $3 0.5% 0.5% $2_1P_even

   /home/vpnserver/Documents/asym_test.sh  $4 $5 0% 0% $2_0_mod
   /home/vpnserver/Documents/asym_test.sh  $4 $5 0.03% 0.07% $2_P1_mod
   /home/vpnserver/Documents/asym_test.sh  $4 $5 0.15% 0.35% $2_P5_mod
   /home/vpnserver/Documents/asym_test.sh  $4 $5 0.3% 0.7% $2_1P_mod

   /home/vpnserver/Documents/asym_test.sh  $6 $7 0% 0% $2_0_sev
   /home/vpnserver/Documents/asym_test.sh  $6 $7 0% 0.1% $2_P1_sev
   /home/vpnserver/Documents/asym_test.sh  $6 $7 0% 0.5% $2_P5_sev
   /home/vpnserver/Documents/asym_test.sh  $6 $7 0% 1% $2_1P_sev


#Bridge: delete tc settings
sshpass -p "mptcp11" ssh -p 22 root@10.8.1.110 "/home/bridge0/Documents/tc_param.sh del eth2 $7 1%; /home/bridge0/Documents/tc_param.sh del eth3 $7 1%; /home/bridge0/Documents/tc_param.sh del eth9 $6 0%; /home/bridge0/Documents/tc_param.sh del eth10 $6 0%; exit"


#kill openvpn on client in preperation for next test
sshpass -p "mptcp11" ssh -p 22 root@10.8.2.2 "pkill openvpn"





