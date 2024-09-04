#pragma once

#include <vector>
#include <functional>
#include <random>
#include <assert.h>
#include <map>
#include <tuple>

template <typename T>
struct Diversity_Preserver {
    int index;
    bool first;
    std::map<std::pair<int, int>, double> diversity_scores;
    std::vector<T> genes;
};

// Class Outline ----------------------------------------------------------------------------------------------------------------------------

template <typename T, typename L>
class Population {

protected:

    std::vector<T> genes;
    std::mt19937 generator;
    int generation;

    // Change from reference to object
    std::function<std::vector<T>(const std::vector<T>&, std::mt19937&)> selectParents;
    std::function<std::vector<T>(const std::vector<T>&, std::mt19937&)> mutate;
    std::function<Diversity_Preserver<T>(const std::vector<T>&, const T&, const Diversity_Preserver<T>&, std::mt19937&)> selectSurvivors;

    Diversity_Preserver<T> div_preserver;

public:

    Population(
        int seed,
        std::function<std::vector<T>(std::mt19937&)> initialize,
        std::function<std::vector<T>(const std::vector<T>&, std::mt19937&)> selectParents,
        std::function<std::vector<T>(const std::vector<T>&, std::mt19937&)> mutate,
        std::function<Diversity_Preserver<T>(const std::vector<T>&, const T&, const Diversity_Preserver<T>&, std::mt19937&)> selectSurvivors
    );

    void execute();   
    void execute(std::function<bool(Population<T,L>&)> termination_criterion);   
    L get_best_fitness(std::function<std::vector<L>(const std::vector<T>&)>& evaluate);                 
    std::vector<T> get_bests(bool keep_duplicats, std::function<std::vector<L>(const std::vector<T>&)>& evaluate);       
    std::vector<T> get_genes(bool keep_duplicats);   
    int get_generation();
    int get_size(bool keep_duplicates);        
    void set_genes(std::vector<T> new_genes);      
    double get_diversity(std::function<double(const std::vector<double>&)> diversity_measure_population);

};

// Class Implementation ---------------------------------------------------------------------------------------------------------------------

template <typename T, typename L>
Population<T, L>::Population(
    int seed,
    std::function<std::vector<T>(std::mt19937&)> initialize,
    std::function<std::vector<T>(const std::vector<T>&, std::mt19937&)> selectParents,
    std::function<std::vector<T>(const std::vector<T>&, std::mt19937&)> mutate,
    std::function<Diversity_Preserver<T>(const std::vector<T>&, const T&, const Diversity_Preserver<T>&, std::mt19937&)> selectSurvivors
) : generation(0), generator(seed), selectParents(selectParents), mutate(mutate), selectSurvivors(selectSurvivors) {
    genes = initialize(generator);
    assert(genes.size() > 0 && "initialize function must return a non-empty vector");
    div_preserver = Diversity_Preserver<T>{0, true, std::map<std::pair<int, int>, double>(), genes};
    div_preserver = selectSurvivors(genes, genes[0], div_preserver, generator);
}

template <typename T, typename L>
void Population<T, L>::execute() {
    generation++;
    std::vector<T> parents = selectParents(genes, generator);
    std::vector<T> children = mutate(parents, generator);
    div_preserver = selectSurvivors(genes, children[0], div_preserver, generator);
    genes = div_preserver.genes;
}

template <typename T, typename L>
void Population<T, L>::execute(std::function<bool(Population<T,L>&)> termination_criterion){
    while(!termination_criterion(*this)){
        execute();
    }
}

template <typename T, typename L>
L Population<T, L>::get_best_fitness(std::function<std::vector<L>(const std::vector<T>&)>& evaluate){
    std::vector<L> fitnesses = evaluate(genes);
    auto min_it = std::min_element(fitnesses.begin(), fitnesses.end());
    return *min_it;
}

template <typename T, typename L>
std::vector<T> Population<T, L>::get_genes(bool keep_duplicats){
    if(keep_duplicats) return genes;
    std::vector<T> genes_copy = genes;
    std::sort(genes_copy.begin(), genes_copy.end());
    genes_copy.erase(std::unique(genes_copy.begin(), genes_copy.end()), genes_copy.end());
    return genes_copy;
}

template <typename T, typename L>
int Population<T, L>::get_generation(){
    return generation;
}

template <typename T, typename L>
int Population<T, L>::get_size(bool keep_duplicates){
    return get_genes(keep_duplicates).size();
}

template <typename T, typename L>
void Population<T, L>::set_genes(std::vector<T> new_genes){
    genes = new_genes;
}

template <typename T, typename L>
double Population<T, L>::get_diversity(std::function<double(const std::vector<double>&)> diversity_measure_population){
    std::vector<double> diversity_scores;
    diversity_scores.reserve(div_preserver.diversity_scores.size()); 
    for (const auto& entry : div_preserver.diversity_scores) {
        const auto& indices = entry.first;
        if (indices.first != div_preserver.index && indices.second != div_preserver.index) {
            diversity_scores.push_back(entry.second);
        }
    }
    return diversity_measure_population(diversity_scores);
}