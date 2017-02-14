This is where you find the necessary shell scripts to run the tests used 
in my thesis.  Here is a breakdown of what each script does:


__VPN Client Scripts:__

* item **vpnstart.sh:** Allows for starting the client side VPN
 remotely from the server using an SSH connection.
 The script will start a Wireshark capture, initiate 
 the tunnel connection, and then conduct a test download.  
 The Wireshark capture allows for verifying the VPN tunnel 
 behaves as expected for the desired test.
    
  
* item **download.sh:** Allows for initiating the 10 downloads 
using *wget* in quiet mode.  This script could easily be 
adjusted to perform any number of downloads required.
Quiet mode was used to prevent unnecessary download 
statistics being reported to the server via the SSH connection.
    


__VPN Server Scripts:__


* **supertest.sh:** This was the master script for conducting 
the symmetric tests of Sections 3.1.4, 3.1.5, and 4.2.
The script allowed for command line arguments to test 
MPTCP, MPUDP, TCP, or UDP.  The user must also specify 
the desired TCP congestion control algorithm to use.  This 
script allowed for ensuring each test had the same starting 
parameters and was conducted properly.
    

* **symm_test.sh:**  Called by the supertest.sh script to 
conduct the required tests.
    
* **asym_supertest.sh:**  Similar to the symmetric 
supertest, but for conducting asymmetric testing of 
Section 3.1.6.
    

* **asym\_test.sh:** Called by the asym_supertest.sh script 
to conduct the required tests.
    

* **subflow_supertest.sh:** This is the master script for 
conducting the subflow tests of Section 3.1.5.
    

* **sub_test.sh** Called by the subflow_supertest.sh script 
to conduct the required tests.
    
* **tcp_dump.sh:** Starts the required Wireshark captures 
for the test.



__Web Server Scripts:__


* **directory_sym.sh** and **directory_asym.sh:** Creates the 
required directories automatically for storing the test data.
This could be done by the user manually, but problems 
result if the user forgets to build all required directories.
    

* **web_tcp_dump.sh:** Starts the required Wireshark captures 
for the test.



__Bridge Machine Scripts:__


* **network_start.sh:** This script was run on machine 
start-up in order to initialize the required bridges 
between the interfaces.  This script also set the 
required speed limits for the interfaces.  To run this 
script at start-up, a configuration file was used.
    
* **tc\_qdisc.sh:** Show and record the traffic control 
settings on each interface.  Allowed for verifying the 
proper settings were in place during each round of testing.
    

* **tc\_param.sh:** Used to add, change, or delete traffic 
control loss rates or delay rates for each interface.
    

* **bridge\_tcp\_dump.sh:** Starts the required Wireshark 
captures for the test.  These Wireshark captures were 
primarily used during initial testing to verify traffic 
was using the VPN tunnel as desired.
    
