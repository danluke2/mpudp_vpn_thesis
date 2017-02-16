# mpudp_vpn_thesis
This project is a result of my Master's thesis from Naval Postgraduate School.  This thesis involved adding a simplified MPUDP protocol to the existing MPTCP Linux kernel and testing MPTCP and MPUDP performance with OpenVPN.  I have provided the shell scripts, code, and my thesis to allow anyone to replicate my work as well as contribute to the MPUDP protocol.


This project relies on the MPTCP kernel available here:https://github.com/multipath-tcp/mptcp

I changed the udp.c file to allow for MPUDP between the VPN client and server.  Simply replace the \net\ipv4\udp.c file with my file and compile the kernel as described by the MPTCP page.

There are 2 Linux kernel modules needed to allow for MPUDP testing (located in c_files):
  
* **MPUDP_recv:** allows for changing the source address of incoming packets to the "master" flow address.  This is needed for OpenVPN to prevent dropping packets from an unknown source.
 
* **MPUDP_send:** allows for probabilistically changing the destination of outgoing packets.  By changing the destination to an alternate address, the packets will be routed over each path available.
  

The topology used for testing can be built physically or through VM's.  All shell code provided is from the physical testbed.  You can modify the code to work better in a virtual environment since you can use a centralized shared folder to hold the test files and results.  The topology used is as follows:

![Alt text](/pics/sim_topology.png?raw=true)



