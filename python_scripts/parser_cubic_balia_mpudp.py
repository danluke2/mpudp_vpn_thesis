'''
Author: LT Lukaszewski
Assisted by: 2LT Warren Barksdale

Purpose: This will parse a directory that has the following folders:
        - 0%
        - 0.1%
        - 0.5%
        - 1%
        Each folder needs a tcp.csv, ndiffports.csv, and fullmesh.csv file.  
        The parser will enter each folder, parse the csv and add values to 
        appropriate list for graphing.

Sections Covered: 3.1.4 (cubic), 3.1.5 (balia), and 4.6 (MPUDP)

Assumes: This script worked for thesis testing and uses these assumptions:
        - folder setup is described as above
        - Testing: 1,10,20,40,60,80,100ms with 10 trials each
        - Address of web server is 10.8.3.3
        
Last Modified: 1/30/2017
'''

import math
import numpy as np
import scipy as sp
import scipy.stats
import os
import matplotlib.pyplot as plt



#List of File Calulations [Filename, Base Directory, [[List of Means] , [List of Conf]]]
fileList = [] 



#gets the mean and confidence interval and returns to caller
def mean_confidence_interval(data, confidence=0.95):
	
    a = 1.0*np.array(data)
    n = len(a)
    m, se = np.mean(a), scipy.stats.sem(a)
    h = se * sp.stats.t._ppf((1+confidence)/2., n-1)
    return m, h


    
#Navigate to main directory
path = os.getcwd()

#Testing folder and subdirectory walking
for root, dirs, files in os.walk(path):
    for name in files:
        #change current directory to the location of the "name" file
        os.chdir(root)
        if name.endswith((".csv")):
            print("Working on file:\n",os.path.join(root, name))
            print("Current Working Directory: ",os.getcwd())
            print("Path to:",name," is \t",root)
            print("\n\n")
		
            results_Tuple = ()
            list1 = []
            refinedList = [] # List of individual row lists

            with open(name, newline='') as csvfile:
                #read line and split by whitespace
                list1=[line.split() for line in csvfile]

			#remove rows that contain useless data
                for x in range(len(list1)):
                    if ((len(list1[x]) != 11) or (list1[x][2] != "10.8.3.3:http")):
                        continue
                    else:
                        refinedList.append(list1[x])

        		#Sorting by second to last column, start time
                refinedList.sort(key=lambda x: float(x[9]))
                
                download=[[],[],[],[],[],[],[]]
                mean_List = []
                conf_List = []
                results=[]

			#average to Mbps	
                for x in range(len(refinedList)):
                    filesize = 0
                    filesize = ((16331410*8)/float(refinedList[x][10]))/math.pow(10,6)
                    #1ms RTT
                    if x<10:
                        download[0].append(filesize)
                    #10ms RTT
                    elif x<20:
                        download[1].append(filesize)
                    #20ms RTT
                    elif x<30:
                        download[2].append(filesize)
                    #40ms RTT
                    elif x<40:
                        download[3].append(filesize)
                    #60ms RTT
                    elif x<50:
                        download[4].append(filesize)
                    #80ms RTT
                    elif x<60:
                        download[5].append(filesize)
                    #100ms RTT
                    elif x<70:
                        download[6].append(filesize)

                #calculate all the means and confidence intervals
                for downl in download:       
                    mean, conf = mean_confidence_interval(downl,0.95)
                    mean_List.append(mean)
                    conf_List.append(conf)
                
                results.append(mean_List)
                results.append(conf_List)
                results_Tuple = (name, os.path.basename(root), results)
                fileList.append(list(results_Tuple))
                csvfile.close()
                
    #i should have 3 files now and graph them           
    if len(fileList) == 3:
        print("3 Files added")
        
        while len(fileList)>0:
            #print the list for detecting errors
            for x in range(len(fileList)):
                print("File:",fileList[x][0],"\nFrom:",fileList[x][1])
                print("\nMean List(X)\t Conf List(Y)")
                
                for z in range(len(fileList[x][2][0])):
                    print(fileList[x][2][0][z],"\t",fileList[x][2][1][z])
                    print("\n")
                    
            #get data for plotting, ecpecting: 
                # TCP, ndiffports, and fullmesh for 3.1.4, 3.1.5
                # UDP, mptcp, MPUDP for 4.6  (mptcp is fullmesh MPTCP)
            mpudp_case = 0;
            for x in fileList:
                if (x[0]=="TCP.csv" or x[0]=="UDP.csv"):
                    y3 = x[2][0]
                    yerr3 = x[2][1]
                    if x[0]=="UDP.csv":
                        mpudp_case = 1
                elif (x[0]=="ndiffports.csv" or x[0]=="mptcp.csv"):
                    y2 = x[2][0]
                    yerr2 = x[2][1]
                elif (x[0]=="fullmesh.csv" or x[0]=="MPUDP.csv"):
                    y = x[2][0]
                    yerr1 = x[2][1]
            
            N = len(y)               
            ind = np.arange(N)       
            margin = 0.2
            width = 0.25
            fig, ax = plt.subplots()
            
            bar1 = ax.bar(ind-0.25, y, width, color='b', yerr=yerr1,
                            error_kw={'ecolor':'k', 'linewidth':2})
            
            bar2 = ax.bar(ind, y2, width, color='r', yerr=yerr2, 
                            error_kw={'ecolor':'k', 'linewidth':2})
            
            bar3 = ax.bar(ind + 0.25, y3, width, color='g', yerr=yerr3, 
                            error_kw={'ecolor':'k', 'linewidth':2})
            
            axes = plt.gca()							    
            axes.set_yticks([0, 3, 6, 9, 12, 15, 18, 21])
            #put a line at single path max
            ax.axhline(10,linestyle='--', color='k')    
            ax.set_ylabel('GOODPUT (Mbps)')
            ax.set_xlabel('Link Propagation RTT (ms)')
            ax.set_xticks(ind+.125)
            ax.set_xticklabels([1,10,20,40,60,80,100])
            if mpudp_case:
                ax.legend((bar1[0], bar2[0], bar3[0]), 
                           ('MPUDP', 'MPTCP', 'UDP'),prop={'size':15})
            else:
                ax.legend((bar1[0], bar2[0], bar3[0]), 
                           ('fullmesh', 'ndiffports', 'TCP'),prop={'size':15})
            
            plt.savefig(fileList[0][1] +'_loss.png')			
            plt.clf()
            fileList.pop(0)
            fileList.pop(0)
            fileList.pop(0)
            print("3 Files Graphed and removed from fileList")
        

#				
