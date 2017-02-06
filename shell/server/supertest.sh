#!/bin/bash

#Settings:
#set desired mem parameters before test
#ensure iptables set for server and client


#Parameters: 
# 1: balia or cubic
# 2+: fullmesh, ndiffports, TCP, UDP, MPUDP
# can start over at 1 at any point (ex: balia fullmesh cubic ndiffports)


#log openvpn files
#we don't want to cache info on tcp sessions since we are running repeated tests

cd /home/vpnserver/Documents/log/
sudo cp /etc/openvpn/tcp443.conf .
sysctl -w net.ipv4.tcp_no_metrics_save=1;

sshpass -p "mptcp11" ssh -p 22 root@10.8.2.2 "sysctl -w net.ipv4.tcp_no_metrics_save=1; cd /home/client/Documents/log/; cp /etc/openvpn/client.ovpn .; exit"


#create folders on server for test
cd /home/vpnserver/Documents/
mkdir run
chmod +777 run
cd run/

for dir in 0% 0.1% 0.5% 1%
   do
     mkdir $dir
     chmod +777 $dir
done

#create folders on web
sshpass -p "mptcp11" ssh -p 22 root@10.8.3.3 "cd /home/web/Documents/;./directory_sym.sh exit"





#start testing, use parameters specified when calling this script
for test
do
 if [ "$test" = "balia" ] || [ "$test" = "cubic" ] 
 then
    sysctl -w net.ipv4.tcp_congestion_control=$test
    sshpass -p "mptcp11" ssh -p 22 root@10.8.2.2 "sysctl -w net.ipv4.tcp_congestion_control=$test; exit"
    continue

 elif [ "$test" = "fullmesh" ] || [ "$test" = "ndiffports" ]
 then
     sshpass -p "mptcp11" ssh -p 22 root@10.8.2.2 "cd /home/client/Documents/log/ ; echo MP $test Parameters >> status; sysctl -w net.mptcp.mptcp_enabled=1 >> status; sysctl -w net.mptcp.mptcp_path_manager=$test >> status; sysctl net.ipv4.tcp_congestion_control >> status; exit"
     cd /home/vpnserver/Documents/log/
     echo CS $test Parameters >> status_$test
     sysctl -w net.mptcp.mptcp_enabled=1 >> status_$test
     sysctl -w net.mptcp.mptcp_path_manager=$test >>status_$test
     sysctl net.ipv4.tcp_congestion_control >> status_$test
     service openvpn restart

     #start tcpdump, start openvpn connection, warmup download, kill tcpdump
     sshpass -p "mptcp11" ssh -p 22 root@10.8.2.2 "cd /home/client/Documents/log/ ; nohup /home/client/Documents/vpnstart.sh $test; exit"


 elif [ "$test" = "MPUDP" ]
 then
     sshpass -p "mptcp11" ssh -p 22 root@10.8.2.2 "cd /home/client/Documents/log/ ; echo MP $test Parameters >> status; sysctl -w net.mptcp.mptcp_enabled=0 >> status; sysctl net.ipv4.tcp_congestion_control >> status; exit"
     cd /home/vpnserver/Documents/log/
     echo CS $test Parameters >> status_$test
     sysctl -w net.mptcp.mptcp_enabled=0 >> status_$test
     sysctl net.ipv4.tcp_congestion_control >> status_$test
     service openvpn restart

     #start tcpdump, start openvpn connection, warmup download, kill tcpdump
     sshpass -p "mptcp11" ssh -p 22 root@10.8.2.2 "cd /home/client/Documents/log/ ; nohup /home/client/Documents/vpnstart.sh $test; exit"


 elif [ "$test" = "TCP" ] || [ "$test" = "UDP" ]
 then
     sshpass -p "mptcp11" ssh -p 22 root@10.8.2.2 "cd /home/client/Documents/log/; echo MP $test Parameters >> status; sysctl -w net.mptcp.mptcp_enabled=0 >> status; sysctl net.ipv4.tcp_congestion_control >> status; exit"
     cd /home/vpnserver/Documents/log/
     echo CS $test Parameters >> status_$test
     sysctl -w net.mptcp.mptcp_enabled=0 >> status_$test
     sysctl net.ipv4.tcp_congestion_control >> status_$test
     service openvpn restart

     #start tcpdump, start openvpn connection, warmup download, kill tcpdump
     sshpass -p "mptcp11" ssh -p 22 root@10.8.2.2 "cd /home/client/Documents/log/ ; nohup /home/client/Documents/vpnstart.sh $test; exit"

 else
     exit 1
 fi

#run various test for current $test value
for i in 0% 0.1% 0.5% 1%
 do
    /home/vpnserver/Documents/symm_test.sh $test $i
 done

 #kill openvpn on client in preperation for next test
 sshpass -p "mptcp11" ssh -p 22 root@10.8.2.2 "pkill openvpn"
done




