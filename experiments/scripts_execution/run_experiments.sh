#!/bin/bash

# preliminary experiments for lambdas
lambdas=("0" "0.1" "0.15" "0.2" "0.4" "0.75" "1" "1.2" "1.5" "2" "2.5" "3")
mus="2,3,5,8"
ns="5,7,10"
ms="1,3"
runs="10"
alphas="0.3,0.6,1"

# actual experiments

output_path="../experiments/data/runs"

chmod +x ./run.sh

euclidean_norm=("0" "1")
for euclidean_norm in "${euclidean_norm[@]}"; do
    for lambda in "${lambdas[@]}"; do
        ./run.sh "$output_path/XRAI_$lambda_$euclidean_norm.csv" "XRAI" $euclidean_norm $runs $mus $ns $ms $alphas $lambda 
    done
    ./run.sh "$output_path/1RAI_$euclidean_norm.csv" "1RAI" $euclidean_norm $runs $mus $ns $ms $alphas "-" 
done