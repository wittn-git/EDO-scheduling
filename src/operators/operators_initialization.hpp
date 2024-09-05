#pragma once

#include <functional>
#include <vector>
#include <random>
#include <algorithm>

using T = std::vector<std::vector<int>>;
using L = int;

//Initialization Operators ----------------------------------------------------------

/*
    Fix Initialization: Initialize genes with a fixed set of genes
    Arguments:
        - genes:            Vector of genes
*/

std::function<std::vector<T>(std::mt19937&)> initialize_fixed(std::vector<T> genes){
    return [genes](std::mt19937& generator) -> std::vector<T> {
        return genes;
    };
}