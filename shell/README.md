This is where you find the necessary shell scripts to run the tests used in my thesis.  Here is a breakdown of what each script does:


\underline{\textbf{\ac{VPN} Client Scripts:}}

\begin{itemize}
    \item \textbf{vpnstart.sh:} Allows for starting the client side \ac{VPN} remotely from the server using an \ac{SSH} connection.  The script will start a Wireshark capture, initiate the tunnel connection, and then conduct a test download.  The Wireshark capture allows for verifying the \ac{VPN} tunnel behaves as expected for the desired test.
    
    \vspace{1.5mm}
    \item \textbf{download.sh:} Allows for initiating the 10 downloads using \emph{wget} in quiet mode.  This script could easily be adjusted to perform any number of downloads required.  Quiet mode was used to prevent unnecessary download statistics being reported to the server via the \ac{SSH} connection.
    
\end{itemize}

\underline{\textbf{\ac{VPN} Server Scripts:}}

\begin{itemize}

    \item \textbf{supertest.sh:} This was the master script for conducting the symmetric tests of Sections \ref{sub:sym-cubic}, \ref{sub:sym-balia}, and \ref{sec:mpudp-imp}.  The script allowed for command line arguments to test \ac{MPTCP}, \ac{MPUDP}, \ac{TCP}, or \ac{UDP}.  The user must also specify the desired \ac{TCP} congestion control algorithm to use.  This script allowed for ensuring each test had the same starting parameters and was conducted properly.
    
    \vspace{1.5mm}
    \item \textbf{symm\_test.sh: } Called by the supertest.sh script to conduct the required tests.
    
    \vspace{1.5mm}
    \item \textbf{asym\_supertest.sh:}  Similar to the symmetric supertest, but for conducting asymmetric testing of Section \ref{sub:asym-tests}.
    
    \vspace{1.5mm}
    \item \textbf{asym\_test.sh} Called by the asym\_supertest.sh script to conduct the required tests.
    
    \vspace{1.5mm}
    \item \textbf{subflow\_supertest.sh:} This is the master script for conducting the subflow tests of Section \ref{sub:add_sub}.
    
    \vspace{1.5mm}
    \item \textbf{sub\_test.sh} Called by the subflow\_supertest.sh script to conduct the required tests.
    
    \vspace{1.5mm}
    \item \textbf{tcp\_dump.sh:} Starts the required Wireshark captures for the test.
\end{itemize}


\underline{\textbf{Web Server Scripts:}}

\begin{itemize}
    \item \textbf{directory\_sym.sh and directory\_asym.sh:} Creates the required directories automatically for storing the test data.  This could be done by the user manually, but problems result if the user forgets to build all required directories.
    
    \vspace{1.3mm}
    \item \textbf{web\_tcp\_dump.sh:} Starts the required Wireshark captures for the test.
    
\end{itemize}


\underline{\textbf{Bridge Machine Scripts:}}

\begin{itemize}
    \item \textbf{network\_start.sh:} This script was run on machine start-up in order to initialize the required bridges between the interfaces.  This script also set the required speed limits for the interfaces.  To run this script at start-up, a configuration file was used.
    
    \vspace{1.3mm}
    \item \textbf{tc\_qdisc.sh:} Show and record the traffic control settings on each interface.  Allowed for verifying the proper settings were in place during each round of testing.
    
    \vspace{1.3mm}
    \item \textbf{tc\_param.sh:} Used to add, change, or delete traffic control loss rates or delay rates for each interface.
    
    \vspace{1.3mm}
    \item \textbf{bridge\_tcp\_dump.sh:} Starts the required Wireshark captures for the test.  These Wireshark captures were primarily used during initial testing to verify traffic was using the \ac{VPN} tunnel as desired.
    
\end{itemize}
