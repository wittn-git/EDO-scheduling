#!/bin/bash

lambdas=("0.1" "1" "1.5")
mus="2,5,10,25"
ns="5,10,15,25,50"
ms="1,3,5"
runs="50"
alphas="0.3,0.6,1"
diversity_operators=("eucl" "sum") # "ord" currently not supported

output_path="../experiments/data/runs"

chmod +x ./run.sh

for diversity_operator in "${diversity_operators[@]}"; do
    for lambda in "${lambdas[@]}"; do
        ./run.sh "$output_path/XRAI-$lambda-$diversity_operator.csv" "XRAI" $diversity_operator $runs $mus $ns $ms $alphas $lambda 
    done
    ./run.sh "$output_path/1RAI-$diversity_operator.csv" "1RAI" $diversity_operator $runs $mus $ns $ms $alphas "-" 
done