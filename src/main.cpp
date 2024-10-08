#include "utility/testing.hpp"
#include "utility/parsing.hpp"

/*
    Parameters (in order):
        - output_file: string
        - Mutation-Operator: {"1RAI", "XRAI"}
        - Diversity-Operator: {"eucl", "sum", "ord"}
        - runs: int
        - mus: mu_1,mu_2,...,mu_w (ints)
        - ns: n_1,n_2,...,n_x (ints)
        - ms: m_1,m_2,...m_y (ints)
        - alphas: a_1,a_2,...,a_z (doubles)
        - lambda: double (only for "XRAI", mean of the poisson distribution, pass "-" if unused)
*/

int main(int argc, char **argv){

    auto [output_file, mutation_operator, mutation_string, diversity_string, runs, mus, ns, ms, alphas] = parse_arguments(argc, argv);
    test_algorithm(mus, ns, ms, alphas, runs, output_file, mutation_string, mutation_operator, diversity_string);
    return 0;
}