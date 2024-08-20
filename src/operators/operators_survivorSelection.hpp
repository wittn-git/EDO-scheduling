#pragma once

#include <functional>
#include <vector>
#include <numeric>
#include <random>
#include <map>
#include <tuple>
#include <assert.h>

#include "operators_diversity.hpp"
#include "../population/population.hpp"

using T = std::vector<std::vector<int>>;
using L = double;

// Survivor selection operators ----------------------------------------------------

/*
    div-Selection: Selects the mu (=parent size) individuals with the highest diversity from the combined population of parents and one offspring, preserve diversity scores to improve runtime
    Arguments
        - diversity_measure:    function taking two genes and returning a double representing the diversity
*/

std::function<Diversity_Preserver<T>(const std::vector<T>&, const T&, const Diversity_Preserver<T>&, std::mt19937&)> select_div(std::function<double(const T&, const T&)> diversity_measure_individual, std::function<double(const std::vector<double>&)> diversity_measure_population) {
    return [diversity_measure_individual, diversity_measure_population](const std::vector<T>& parents, const T& offspring, const Diversity_Preserver<T>& diversity_preserver, std::mt19937& generator) -> Diversity_Preserver<T> {
        std::vector<T> selected_genes = parents;
        selected_genes.emplace(selected_genes.begin() + diversity_preserver.index, offspring);

        std::map<std::pair<int, int>, double> diversity_scores;
        if(diversity_preserver.first){
            for(int i = 0; i < selected_genes.size(); i++){
                for(int j = i + 1; j < selected_genes.size(); j++){
                    diversity_scores[{i,j}] = diversity_measure_individual(selected_genes[i], selected_genes[j]);
                }
            }
        }else{
            diversity_scores = diversity_preserver.diversity_scores;
            for(int i = 0; i < diversity_preserver.index; i++){
                diversity_scores[{i,diversity_preserver.index}] = diversity_measure_individual(selected_genes[i], selected_genes[diversity_preserver.index]);
            }
            for(int i = diversity_preserver.index + 1; i < selected_genes.size(); i++){
                diversity_scores[{diversity_preserver.index,i}] = diversity_measure_individual(selected_genes[diversity_preserver.index], selected_genes[i]);
            }
        }
        
        std::vector<int> indices(selected_genes.size());
        std::iota(indices.begin(), indices.end(), 0);
        std::shuffle(indices.begin(), indices.end(), generator);

        std::vector<double> diversity_values;
        diversity_values.reserve(indices.size());
        for (const auto& index : indices) {
            std::vector<double> div_vector;
            div_vector.reserve(indices.size());
            auto isIndexExcluded = [&index](const auto& entry) {
                const auto& [firstIndex, secondIndex] = entry.first;
                return (firstIndex != index) && (secondIndex != index);
            };
            for (const auto& entry : diversity_scores) {
                if (isIndexExcluded(entry)) {
                    div_vector.push_back(entry.second);
                }
            }
            diversity_values[index] = diversity_measure_population(div_vector);
        }
        auto max_it = std::max_element(indices.begin(), indices.end(), [&](int a, int b) {
            return diversity_values[a] <= diversity_values[b];
        });
        selected_genes.erase(selected_genes.begin() + *max_it);
        return { *max_it, false, diversity_scores, selected_genes };
    };
}

/*
    div-Selection: Selects the mu (=parent size) individuals with the highest diversity from the combined population of parents and offspring, if quality of offspring is at least alpha * ( n - OPT ) + OPT), preserve diversity scores to improve runtime
    Arguments:
        - alpha:                parameter for quality threshold
        - n:                    number of jobs
        - OPT:                  fitness value of optimal solution
        - diversity_measure:    function taking two genes and returning a double representing the diversity
        - evaluate:             function taking a vector of genes and returning a vector of fitnesses
*/
std::function<Diversity_Preserver<T>(const std::vector<T>&, const T&, const Diversity_Preserver<T>&, std::mt19937&)> select_div(double alpha, int n, double OPT, std::function<double(const T&, const T&)> diversity_measure_individual, std::function<double(const std::vector<double>&)> diversity_measure_population, std::function<std::vector<L>(const std::vector<T>&)> evaluate) {
    return [alpha, n, OPT, diversity_measure_individual, diversity_measure_population, evaluate](const std::vector<T>& parents, const T& offspring, const Diversity_Preserver<T>& diversity_preserver, std::mt19937& generator) -> Diversity_Preserver<T> {
        if(evaluate({offspring})[0] > alpha * ( n - OPT ) + OPT) return diversity_preserver;
        std::function<Diversity_Preserver<T>(const std::vector<T>&, const T&, const Diversity_Preserver<T>&, std::mt19937&)> div = select_div(diversity_measure_individual, diversity_measure_population);
        return div(parents, offspring, diversity_preserver, generator);
    };
};