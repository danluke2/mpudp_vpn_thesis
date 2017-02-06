#!/bin/bash


#Purpose: perform 10 downloads of test file 
#could change 10 to be shell variable



echo starting downloads

for i in {1..10}; do
wget -q http://10.8.3.3/test/test16.txt -O /dev/null;

done



