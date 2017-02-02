'''
Author: LT Lukaszewski
Assisted by: 2LT Warren Barksdale

Purpose: This will parse a directory that has the following folders:
        - 0%
        - 0.1%
        - 0.5%
        - 1%
        Each folder needs a tcp.csv, fullmesh.csv, and fullmesh_2-5 files.  
        The parser will enter each folder, parse the csv and add values to 
        appropriate list for normalization and then graphing.

Figure Covered: 3.7 (fullmesh subflows)

Assumes: This script worked for thesis testing and uses these assumptions:
        - folder setup is described as above
        - Testing: 1,10,20,40,60,80,100ms with 10 trials each
        - Address of web server is 10.8.3.3
        
Last Modified: 2/2/2017
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
    
    #i should have 6 files now and graph them           
    if len(fileList) == 6:
        print("6 Files added")
        
        while len(fileList)>0:
            #print the list for detecting errors
            for x in range(len(fileList)):
                print("File:",fileList[x][0],"\nFrom:",fileList[x][1])
                print("\nMean List(X)\t Conf List(Y)")
                
                for z in range(len(fileList[x][2][0])):
                    print(fileList[x][2][0][z],"\t",fileList[x][2][1][z])
                    print("\n")
            
            #get data for plotting, ecpecting: 
            # TCP, fullmesh, and fullmesh_2-5 for Figure 3.7       
            for x in fileList:
                if x[0]=="tcp.csv":
                    yTcp = x[2][0]
                    yerrTcp = x[2][1]
                elif x[0]=="fullmesh_2.csv":
                    y2 = x[2][0]
                    yerr2 = x[2][1]
                elif x[0]=="fullmesh_3.csv":
                    y3 = x[2][0]
                    yerr3 = x[2][1]
                elif x[0]=="fullmesh_4.csv":
                    y4 = x[2][0]
                    yerr4 = x[2][1]
                elif x[0]=="fullmesh_5.csv":
                    y5 = x[2][0]
                    yerr5 = x[2][1]
                else:
                    y = x[2][0]
                    yerr1 = x[2][1]				
                
                #[[data],[up error], [down error]]
                fm = [[],[],[]] 
                fm2 = [[],[],[]]
                fm3 = [[],[],[]]
                fm4 = [[],[],[]]
                fm5 = [[],[],[]]

                #copy error data into lists so can be normalized
                for x in range(len(yerr1)):
                    fm[1].append(yerr1[x]+y[x])
                    fm[2].append(y[x]-yerr1[x])

                    fm2[1].append(yerr2[x]+y2[x])
                    fm2[2].append(y2[x]-yerr2[x])
                    fm3[1].append(yerr3[x]+y3[x])
                    fm3[2].append(y3[x]-yerr3[x])
                    fm4[1].append(yerr4[x]+y4[x])
                    fm4[2].append(y4[x]-yerr4[x])
                    fm5[1].append(yerr5[x]+y5[x])
                    fm5[2].append(y5[x]-yerr5[x])
                
                #normalize the data
                for x in range(len(y)):
                    imp = (float(y[x]/yTcp[x])-1)*100
                    fm[1][x] = ((float(fm[1][x]/yTcp[x])-1)*100)-imp
                    fm[2][x] = imp-((float(fm[2][x]/yTcp[x])-1)*100)
                    fm[0].append(imp)

                    imp = (float(y2[x]/yTcp[x])-1)*100
                    fm2[1][x] = ((float(fm2[1][x]/yTcp[x])-1)*100)-imp
                    fm2[2][x] = imp-((float(fm2[2][x]/yTcp[x])-1)*100)
                    fm2[0].append(imp)

                    imp = (float(y3[x]/yTcp[x])-1)*100
                    fm3[1][x] = ((float(fm3[1][x]/yTcp[x])-1)*100)-imp
                    fm3[2][x] = imp-((float(fm3[2][x]/yTcp[x])-1)*100)
                    fm3[0].append(imp)

                    imp = (float(y4[x]/yTcp[x])-1)*100
                    fm4[1][x] = ((float(fm4[1][x]/yTcp[x])-1)*100)-imp
                    fm4[2][x] = imp-((float(fm4[2][x]/yTcp[x])-1)*100)
                    fm4[0].append(imp)

                    imp = (float(y5[x]/yTcp[x])-1)*100
                    fm5[1][x] = ((float(fm5[1][x]/yTcp[x])-1)*100)-imp
                    fm5[2][x] = imp-((float(fm5[2][x]/yTcp[x])-1)*100)
                    fm5[0].append(imp)
                    
                    
                    
                N = len(y)               
                ind = np.arange(N)

                x=[1,10,20,40,60,80,100]
                plt.errorbar(x,fm5[0],yerr=[fm5[2],fm5[1]],fmt='-rd', 
                             ecolor='k', label='FM_5')
                plt.errorbar(x,fm4[0],yerr=[fm4[2],fm4[1]],fmt='--gv', 
                             ecolor='k', label='FM_4')
                plt.errorbar(x,fm3[0],yerr=[fm3[2],fm3[1]],fmt='-.b^', 
                             ecolor='k', label='FM_3')
                plt.errorbar(x,fm2[0],yerr=[fm2[2],fm2[1]],fmt='-d', 
                             ecolor='k', color='darkolivegreen', label='FM_2')
                plt.errorbar(x,fm[0],yerr=[fm[2],fm[1]],fmt='--mv', 
                             ecolor='k', label='FM_Default')

                axes = plt.gca()
                axes.set_ylim([0,200])
                axes.set_yticks([0,50,100,150,200])			    

                axes.axhline(100,linestyle='--', color='k')
			    
                plt.ylabel('Percent Difference From TCP (%)')
                plt.xlabel('Link Propagation RTT (ms)')
							    
							    
                plt.axis([0,101,0,250])
                plt.legend()			    

                plt.savefig(fileList[0][1] +'_loss.png')			
                plt.clf()

                #romove files from list so can plot next set of 6
                i=0
                while (i<6):
                    fileList.pop(0)
                    i+=1

                print("6 Files Graphed and removed from fileList")

				
