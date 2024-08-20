#include <iostream>

#include "../population/population.hpp"
#include "../operators/operators_initialization.hpp"
#include "../operators/operators_evaluation.hpp"
#include "../operators/operators_parentSelection.hpp"
#include "../operators/operators_mutation.hpp"
#include "../operators/operators_survivorSelection.hpp"
#include "../operators/operators_termination.hpp"

using T = std::vector<std::vector<int>>;
using L = double;

bool check_robustness(const std::vector<T>& population, const std::tuple<int, int>& restricted_jobs){
    for(std::vector<std::vector<int>> gene : population){
        for(std::vector<int> machine : gene){
            if (machine.size() < 2) continue;
            for(int i = 0; i < machine.size()-1; i++){
                if(machine[i] == std::get<0>(restricted_jobs) && machine[i+1] == std::get<1>(restricted_jobs)) return true;
            }
        }
    }
    return false;
}

std::tuple<Population<T,L>, bool, bool> mu1(
    int seed, 
    int m, 
    int n, 
    int mu,
    std::function<bool(Population<T,L>&)> termination_criterion,
    std::function<std::vector<L>(const std::vector<T>&)> evaluate,
    std::function<std::vector<T>(const std::vector<T>&, std::mt19937&)> mutate,
    std::function<double(const T&, const T&)> diversity_measure_individual,
    std::function<double(const std::vector<double>&)> diversity_measure_population,
    double alpha,
    T initial_gene,
    std::tuple<int, int> restricted_jobs
){

    double OPT = evaluate({initial_gene})[0];

    std::function<std::vector<T>(std::mt19937&)> initialize = initialize_fixed(std::vector<T>(mu, initial_gene));
    std::function<std::vector<T>(const std::vector<T>&, const std::vector<L>&, std::mt19937&)> select_parents =  select_random(1);
    std::function<Diversity_Preserver<T>(const std::vector<T>&, const T&, const Diversity_Preserver<T>&, std::mt19937&)> select_survivors = select_div(alpha, n, OPT, diversity_measure_individual, diversity_measure_population, evaluate);

    Population<T,L> population(seed, initialize, evaluate, select_parents, mutate, select_survivors);
    bool starting_robustness = check_robustness(population.get_genes(false), restricted_jobs);

    population.execute(termination_criterion);
    bool ending_robustness = check_robustness(population.get_genes(false), restricted_jobs);

    return std::make_tuple(population, starting_robustness, ending_robustness);
}