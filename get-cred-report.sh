#!/bin/bash
 
declare -a ProfileArray=(masteracc memberacc1 memberacc2 memberacc3 memberacc4 memberacc5 memberacc6 memberacc7)
 
for profile in "${ProfileArray[@]}"; do
     echo -e "\nListing Users in AWS account '$profile'..."
     aws iam get-credential-report --profile $profile | ./parse_credential_report.py > ~/Documents/$profile.csv
done
