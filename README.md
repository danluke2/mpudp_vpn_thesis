# mpudp_vpn_thesis
Adding MPUDP to MPTCP Linux Kernel, testing VPN performance, Master's Thesis 


This project relies on the MPTCP kernel available here:https://github.com/multipath-tcp/mptcp

I changed the udp.c file to allow for MPUDP between the VPN client and server.  Simply replace the \net\ipv4\udp.c file with my file and compile the kernel as described by the MPTCP page.

There are 2 Linux kernel modules needed to allow for MPUDP testing:
  
  -MPUDP_recv: allows for changing the source address of incoming packets to the "master" flow address.  This is needed for OpenVPN to prevent dropping packets from an unknown source.
 
 -MPUDP_send: allows for probabilistically changing the destination of outgoing packets.  By changing the destination to an alternate address, the packets will be routed over each path available.
  

