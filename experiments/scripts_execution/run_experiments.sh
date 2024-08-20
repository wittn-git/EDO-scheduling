#!/bin/bash

operators=("XRAI" "1RAI")
lambdas=("0.1" "0.2")
mus="2,5,10,20,25"
ns="5,10,20,50"
ms="1,3,5"
runs="20"
alphas="0.3,0.6,1"
# TODO substitute lambdas

output_path="../experiments/data/runs"

chmod +x ./run.sh

total_runs=$(( ${#lambdas[@]} + 1 ))
current_run=0
for operator in "${operators[@]}"; do
    if [ "$operator" == "XRAI" ]; then
        for lambda in "${lambdas[@]}"; do
            ./run.sh "$output_path/XRAI_$lambda.csv" $operator $runs $mus $ns $ms $alphas $lambda
        done
    elif [ "$operator" == "1RAI" ]; then
        ./run.sh "$output_path/1RAI.csv" $operator $runs $mus $ns $ms $alphas "-"
    fi
done