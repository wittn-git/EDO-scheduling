#pragma once

#include <iostream>
#include <chrono>

#include "../algorithms/mu1.hpp"
#include "../utility/generating.hpp"
#include "../utility/documenting.hpp"
#include "../utility/solvers.hpp"

using T = std::vector<std::vector<int>>;
using L = double;

// Utility function for testing -----------------------------------------------------

int generate_seed(int mu, int n, int m, double alpha, int run){
    return n*mu*mu+n*run*run+n+m*run+m*m+run + alpha*100*run*n; 
}

bool is_viable_combination(int mu, int n, int m){
    return (m < n) && (mu <= (n*n - n)/(n-m));
}

void loop_parameters(std::vector<int> mus, std::vector<int> ns, std::vector<int> ms, std::vector<double> alphas, int runs, std::function<void(int, int, int, int, float)> func){
    int total_runs = ns.size()*mus.size()*ms.size()*alphas.size()*runs;
    #pragma omp parallel for collapse(4)
    for(int n : ns){
        for(int mu : mus){
            for(int m : ms){
                for(float alpha : alphas){
                    for(int run = 0; run < runs; run++){
                        func(mu, n, m, alpha, run);
                    }
                }
            }
        }
    }
}

std::tuple<int, T> get_optimal_solution(MachineSchedulingProblem problem, int m, std::function<std::vector<L>(const std::vector<T>&)> evaluate) {
    T optimal_solution;
    if (m == 1) optimal_solution = {moores_algorithm(problem)};
    else optimal_solution = approximation_algorithm(problem, m);
    int OPT = evaluate({optimal_solution})[0];
    return std::make_tuple(OPT, optimal_solution);
}

std::tuple<std::function<std::vector<L>(const std::vector<T>&)>, std::function<double(const T&, const T&)>, std::function<double(const std::vector<T>&)>> get_eval_div_funcs(MachineSchedulingProblem problem){
    std::function<std::vector<L>(const std::vector<T>&)> evaluate = evaluate_tardyjobs(problem);
    std::function<double(const T&, const T&)> diversity_measure = diversity_DFM();
    std::function<double(const std::vector<T>&)> diversity_value = diversity_vector(diversity_measure);
    return std::make_tuple(evaluate, diversity_measure, diversity_value);
}

std::tuple<int, int> get_restricted_jobs(int n, int seed){
    std::mt19937 gen(seed);
    std::uniform_int_distribution<int> dist(0, n-1);
    int job1 = dist(gen);
    int job2 = dist(gen);
    while(job1 == job2) job2 = dist(gen);
    return std::make_tuple(job1, job2);
}

// Test functions ------------------------------------------------------------------

void test_algorithm(std::vector<int> mus, std::vector<int> ns, std::vector<int> ms, std::vector<double> alphas, int runs, std::string output_file, std::string operator_string, std::function<std::vector<T>(const std::vector<T>&, std::mt19937&)> mutation_operator){
   
    std::string header = get_csv_line("seed,mu,n,m,alpha,run,generations,max_generations,diversity,fitness,opt,mutation,starting_robustness,ending_robustness");
    write_to_file(header, output_file, false);
    int max_processing_time = 50;

    auto algorithm_test = [output_file, max_processing_time, mutation_operator, operator_string](int mu, int n, int m, float alpha, int run) {

        if(!is_viable_combination(mu, n, m)) return;

        int seed = generate_seed(mu, n, m, alpha, run);
        MachineSchedulingProblem problem = get_problem(seed, n, max_processing_time);
        auto [evaluate, diversity_measure, diversity_value] = get_eval_div_funcs(problem);
        auto [OPT, optimal_solution] = get_optimal_solution(problem, m, evaluate);
        std::tuple<int, int> restricted_jobs = get_restricted_jobs(n, seed);
        
        auto [population, starting_robustness, ending_robustess] = mu1(
            seed, m, n, mu,
            terminate_diversitygenerations(1, true, diversity_measure, 200*n*n*mu), evaluate, mutation_operator, diversity_measure,
            alpha, optimal_solution,
            restricted_jobs
        ); // TODO insert the iteration limit
        std::string result = get_csv_line(seed, mu, n, m, alpha, run, population.get_generation(), 200*n*n*mu, diversity_value(population.get_genes(true)), population.get_best_fitness(evaluate), OPT, operator_string, starting_robustness, ending_robustess); // TODO insert the iteration limit
        write_to_file(result, output_file);
    };

    loop_parameters(mus, ns, ms, alphas, runs, algorithm_test);
}