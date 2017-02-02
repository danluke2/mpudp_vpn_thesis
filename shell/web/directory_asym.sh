#!/bin/bash

#Purpose: create the directories needed for the asymmetric tests

mkdir test
chmod +777 test
cd test/
for dir in $1_0_even $1_P1_even $1_P5_even $1_1P_even $1_0_mod $1_P1_mod $1_P5_mod $1_1P_mod $1_0_sev $1_P1_sev $1_P5_sev $1_1P_sev
do
   mkdir $dir
   chmod +777 $dir
done


