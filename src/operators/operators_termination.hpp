#pragma once

#include <functional>
#include <vector>

#include "../population/population.hpp"
#include "../operators/operators_diversity.hpp"

using T = std::vector<std::vector<int>>;
using L = double;

// Termination operators ------------------------------------------------------

/*
    Diversity or generation termination: Terminate when the diversity is higher than a certain threshold or after a certain number of generations.
    Args:
        threshold:          threshold for the diversity
        diversity_measure:  diversity measure to use
        max_generations:    maximum number of generations
*/
std::function<bool(Population<T,L>&)> terminate_diversitygenerations(double diversity_threshold, std::function<double(const std::vector<double>&)> diversity_measure_population, int generation_threshold){
    return [diversity_measure_population, diversity_threshold, generation_threshold](Population<T,L>& population) -> bool {
        if(population.get_generation() >= generation_threshold) return true;
        if(population.get_diversity(diversity_measure_population) >= diversity_threshold) return true;
        return false;
    };
}