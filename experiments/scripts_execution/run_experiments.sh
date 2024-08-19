#!/bin/bash

operators=("XRAI" "1RAI")
lambdas=("0.1" "0.2" "0.5" "1" "2")
mus="2,3,5"
ns="5,7,10"
ms="1,3"
runs="30"
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