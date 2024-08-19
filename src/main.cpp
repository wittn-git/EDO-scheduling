#include "utility/testing.hpp"
#include "utility/parsing.hpp"

/*
    Parameters (in order):
        - output_file: String
        - Mutation-Operator: {"1RAI", "XRAI"}
        - runs: int
        - mus: mu_1,mu_2,...,mu_w
        - ns: n_1,n_2,...,n_x
        - ms: m_1,m_2,...m_y
        - alpha: a_1,a_2,...,a_z
        - lambda: Double (only for "XRAI", mean of the poisson distribution)
*/

int main(int argc, char **argv){

    auto [mutation_operator, output_file, mus, ns, ms, alphas, runs, operator_string] = parse_arguments(argc, argv);

    test_algorithm(mus, ns, ms, alphas, runs, output_file, operator_string, mutation_operator);
  
    return 0;
}