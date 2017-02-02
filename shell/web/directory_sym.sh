#!/bin/bash

#Purpose: create the directories needed for the symmetric tests

mkdir run
chmod +777 run
cd test/
for dir in 0% 0.1% 0.5% 1%
   do
      mkdir $dir
      chmod +777 $dir
done


