#!/bin/bash

lambdas=() # TODO insert lambdas
mus="2,5,10,25"
ns="5,10,20,50"
ms="1,3,5"
runs="30"
alphas="0.3,0.6,1"

output_path="../experiments/data/runs"

chmod +x ./run.sh

euclidean_norm=("0" "1")
for euclidean_norm in "${euclidean_norm[@]}"; do
    for lambda in "${lambdas[@]}"; do
        ./run.sh "$output_path/XRAI_$lambda_$euclidean_norm.csv" "XRAI" $euclidean_norm $runs $mus $ns $ms $alphas $lambda 
    done
    ./run.sh "$output_path/1RAI_$euclidean_norm.csv" "1RAI" $euclidean_norm $runs $mus $ns $ms $alphas "-" 
done