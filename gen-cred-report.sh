#!/bin/bash
 
declare -a ProfileArray=(masteracc memberacc1 memberacc2 memberacc3 memberacc4 memberacc5 memberacc6 memberacc7)
 
for profile in "${ProfileArray[@]}"; do
     echo -e "\nGenerating credentials report for '$profile'..." >
     aws iam generate-credential-report --profile $profile
     sleep 1
done
