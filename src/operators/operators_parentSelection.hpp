#pragma once

#include <functional>
#include <vector>
#include <random>
#include <assert.h>

using T = std::vector<std::vector<int>>;
using L = double;

/*
    Random Parent Selection: Select subgroup of specified size randomly
    Arguments:
        - parent_size: number of individuals to select
*/

std::function<std::vector<T>(const std::vector<T>&, const std::vector<L>&, std::mt19937&)> select_random(int parent_count) {
    return [parent_count](const std::vector<T>& genes, const std::vector<L>& fitnesses, std::mt19937& generator) -> std::vector<T> {
        std::vector<T> selected_genes(parent_count);
        std::uniform_int_distribution< int > distribute_point(0, genes.size() - 1 );
        std::transform(selected_genes.begin(), selected_genes.end(), selected_genes.begin(), [&](T& selected_gene) mutable -> T {
            int rand_index = distribute_point(generator);
            return genes[rand_index];
        });
        return selected_genes;
    };
}