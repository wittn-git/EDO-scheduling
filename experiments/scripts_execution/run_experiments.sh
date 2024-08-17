#!/bin/bash

mutation_operators=("1RAI" "XRAI")
mus="2,10,25"
ns="5,10,25,50"
ms="1,3,5"
runs="30"
alphas="0.3 0.6 1"
lambdas="0.1 1" 
# TODO substitute lambdas

output_path="../data/runs"

for mutation_operator in "${mutation_operators[@]}"; do
    if [ "$mutation_operator" == "XRAI" ]; then
        current_lambdas="$lambdas"
    elif [ "$mutation_operator" == "1RAI" ]; then
        current_lambdas="-"
    fi
    ./run.sh "$output_path/$mutation_operator" $mutation_operator $runs $mus $ns $ms $alphas $current_lambdas
done