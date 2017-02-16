To implement the MPUDP protocol, we chose to use two 
Linux kernel modules in conjunction with a modification 
to the UDP kernel file.  This method is similar to the 
MPTCP implementation.  We used multiple kernel modules 
in order to simplify the design and clearly delineate the 
purpose of each module. We will now provide a description 
of the C files used for implementing the MPUDP protocol.

__MPUDP C Files:__

* **udp.c:**  The udp.c file is found in directory 
\net\ipv4\ .  This file was modified to include branches 
in the udp\_recmsg and udp\_sendmsg functions.  Code was 
also added to export symbols of functions used in the 
kernel modules.

* **MPUDP\_send.c:** This was the kernel module used to 
implement the MPUDP send function called in the 
udp\_sendmsg function.

* **MPUDP\_recv.c:** This was the kernel module used to 
implement the MPUDP receive function called in the 
udp\_recmsg function.

* **Makefile:** Creates the kernel object files from the 
MPUDP\_send.c and MPUDP\_recv.c files.  The ".ko" files 
are the kernel files inserted to allow for the MPUDP 
functions to work.
