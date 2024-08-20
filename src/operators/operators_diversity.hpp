#pragma once

#include <numeric>
#include <cmath>
#include <limits>
#include <vector>
#include <functional>

using T = std::vector<std::vector<int>>;
using L = double;

// Utility ---------------------------------------------------------------------------

double euclideanNorm(const std::vector<double>& vec) {
    double sumOfSquares = 0.0;
    for (const double& num : vec)
        sumOfSquares += num * num;
    return std::sqrt(sumOfSquares);
}

// Diversity measure operators (gene level) ------------------------------------------

std::function<double(const T& , const T&)> diversity_individual_DFM(){
    return [](const T& gene1, const T& gene2) -> double {
        int common_DFS = 0;
        for (const auto& machine1 : gene1) {
            for (const auto& machine2 : gene2) {
                for(int i = 0; i < machine1.size() - 1; i++){
                    for(int j = 0; j < machine2.size() - 1; j++){
                        if(machine1[i] == machine2[j] && machine1[i+1] == machine2[j+1]){
                            common_DFS++;
                        }
                    }
                }
                if (machine1.back() == machine2.back()) common_DFS++;
            }
        }
        return common_DFS;
    };
}

// Diversity measure operators (population level) --------------------------------------

std::function<double(const std::vector<double>&)> diversity_population_sum(double max_value){
    return [max_value](const std::vector<double>& diversity_scores) -> double {
        double summed_entries = std::accumulate(diversity_scores.begin(), diversity_scores.end(), 0.0);
        return 1 - (summed_entries / max_value);
    };
}

std::function<double(const std::vector<double>&)> diversity_population_eucl(double max_value){
    return [max_value](const std::vector<double>& diversity_scores) -> double {
        return 1 - (euclideanNorm(diversity_scores) / max_value);
    };
}