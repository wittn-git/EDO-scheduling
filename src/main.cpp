#include "utility/testing.hpp"
#include "utility/parsing.hpp"

/*
    Parameters (in order):
        - output_file: String
        - Mutation-Operator: {"1RAI", "XRAI"}
        - euclidean_norm : Bool
        - runs: int
        - mus: mu_1,mu_2,...,mu_w
        - ns: n_1,n_2,...,n_x
        - ms: m_1,m_2,...m_y
        - alphas: a_1,a_2,...,a_z
        - lambda: Double (only for "XRAI", mean of the poisson distribution)
*/

int main(int argc, char **argv){

    auto [output_file, mutation_operator, operator_string, euclidean_norm, runs, mus, ns, ms, alphas] = parse_arguments(argc, argv);

    test_algorithm(mus, ns, ms, alphas, runs, output_file, operator_string, mutation_operator, euclidean_norm);
  
    return 0;
}