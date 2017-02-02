'''
Author: LT Lukaszewski

Purpose: This will parse a directory that has the following csv files for each
         packet loss rate (0, 0.1, 0.5, 1%):
        - even
        - mod
        - severe
        - 1%  
        The parser will enter each csv file, parse the csv and add values to 
        appropriate list for graphing.

Sections Covered: 3.1.6 (assym testing)

Assumes: This script worked for thesis testing and uses these assumptions:
        - folder setup is described as above
        - Testing parameters per Table 3.3
        - Address of web server is 10.8.3.3
        
Last Modified: 2/2/2017
'''



#Assisted by 2LT Warren Barksdale




#Access CSV											DONE
#Parse the single line into columns					DONE
#Sort by start time									DONE
#Get Duration										DONE
#Compute Goodput									DONE
#Crawl through all subdirectories and analyze files DONE
#In each directory generate a plot
 

import math
import numpy as np
import scipy as sp
import scipy.stats
import os
import matplotlib.pyplot as plt




#List of File Calulations [Filename, Base Directory, [[List of Means] , [List of Conf]]]
fileList = []  

even=[0,0,0,0]
even_err=[0,0,0,0]
weak=[0,0,0,0]
weak_err=[0,0,0,0]
strong=[0,0,0,0]
strong_err=[0,0,0,0]


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

        		#Sorting by second to last column 
                refinedList.sort(key=lambda x: float(x[9]))

                download=[]
                mean_List = []
                conf_List = []
                results=[]

			#average to Mbps	
                for x in range(len(refinedList)):
                    filesize = 0
                    filesize = ((16331410*8)/float(refinedList[x][10]))/math.pow(10,6)
                    download.append(filesize)
                
                #each file has 10 downloads.  Need to determine which
                #file they came from to put in correct list
                mean, conf = mean_confidence_interval(download,0.95)
                if name.endswith(("0_even.csv")):
                    even[0]=mean
                    even_err[0]=conf
                elif name.endswith(("1_even.csv")):
                    even[1]=mean
                    even_err[1]=conf
                elif name.endswith(("5_even.csv")):
                    even[2]=mean
                    even_err[2]=conf
                elif name.endswith(("1P_even.csv")):
                    even[3]=mean
                    even_err[3]=conf
                    
                if name.endswith(("0_mod.csv")):
                    weak[0]=mean
                    weak_err[0]=conf
                elif name.endswith(("1_mod.csv")):
                    weak[1]=mean
                    weak_err[1]=conf
                elif name.endswith(("5_mod.csv")):
                    weak[2]=mean
                    weak_err[2]=conf
                elif name.endswith(("1P_mod.csv")):
                    weak[3]=mean
                    weak_err[3]=conf 
                
                if name.endswith(("0_sev.csv")):
                    strong[0]=mean
                    strong_err[0]=conf
                elif name.endswith(("1_sev.csv")):
                    strong[1]=mean
                    strong_err[1]=conf
                elif name.endswith(("5_sev.csv")):
                    strong[2]=mean
                    strong_err[2]=conf
                elif name.endswith(("1P_sev.csv")):
                    strong[3]=mean
                    strong_err[3]=conf
                

                csvfile.close()
 
            
x=[0,0.1,0.5,1.0]    
y=even[:]
y2=weak[:]
y3=strong[:]
yerr1=even_err[:]
yerr2=weak_err[:]
yerr3=strong_err[:]



  
N = len(y)            
ind = np.arange(N)

plt.errorbar(x,y3,yerr=yerr1,fmt='-rd',ecolor='k', label='Severe')
plt.errorbar(x,y2,yerr=yerr2,fmt='--gv',ecolor='k', label='Moderate')
plt.errorbar(x,y,yerr=yerr3,fmt='-.b^',ecolor='k', label='Even')
#plt.errorbar(x,y3[1],yerr=yerr3[1],fmt='-d',ecolor='k',color='darkolivegreen')
#plt.errorbar(x,y3[2],yerr=yerr3[2],fmt='--mv',ecolor='k')
#plt.errorbar(x,y3[3],yerr=yerr3[3],fmt='-.c^',ecolor='k')
  

axes = plt.gca()
axes.set_ylim([0, 17])     
axes.set_yticks([0, 5, 10, 15])

axes.set_xticks([0.0, 0.1, 0.5, 1])
axes.axhline(10,linestyle='--', color='k')

plt.axis([-0.1, 1.1, 0, 17])  
plt.ylabel('GOODPUT (Mbps)')
plt.xlabel('Loss Rate (%)')

plt.legend(loc='lower left',prop={'size':15})                     

plt.savefig('_asym_balia.png')
plt.clf()
