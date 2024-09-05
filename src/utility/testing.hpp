#pragma once

#include <iostream>

#include "../algorithms/mu1.hpp"
#include "../utility/generating.hpp"
#include "../utility/documenting.hpp"
#include "../utility/solvers.hpp"

using T = std::vector<std::vector<int>>;
using L = int;

// Utility function for testing -----------------------------------------------------

int generate_seed(int mu, int n, int m, double alpha, int run){
    return n*mu*mu+n*run*run+n+m*run+m*m+run + alpha*100*run*n; 
}

bool is_viable_combination(int mu, int n, int m){
    return (m < n) && (mu <= (n*n - n)/(n-m));
}

void loop_parameters(std::vector<int> mus, std::vector<int> ns, std::vector<int> ms, std::vector<double> alphas, int runs, std::function<void(int, int, int, int, float)> func){
    int total_runs = ns.size()*mus.size()*ms.size()*alphas.size()*runs;
    #pragma omp parallel for collapse(5)
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

std::tuple<std::function<std::vector<L>(const std::vector<T>&)>, std::function<double(const T&, const T&)>, std::function<double(const std::vector<int>&)>> get_eval_div_funcs(MachineSchedulingProblem problem, std::string diversity_string, int mu, int n){
    std::function<std::vector<L>(const std::vector<T>&)> evaluate = evaluate_tardyjobs(problem);
    std::function<double(const T&, const T&)> diversity_measure_individual = diversity_individual_DFM();
    std::function<double(const std::vector<int>&)> diversity_measure_population;
    if (diversity_string == "eucl"){
        double max_value = (n * std::sqrt((mu * mu - mu)/2));
        diversity_measure_population = diversity_population_eucl(max_value);
    }else if (diversity_string == "sum"){
        double max_value = ((mu * mu - mu)/2)*n;
        diversity_measure_population = diversity_population_sum(max_value);
    }else if (diversity_string == "ord"){
        diversity_measure_population = diversity_population_ord((mu * mu - mu)/2, n);
    }
    return std::make_tuple(evaluate, diversity_measure_individual, diversity_measure_population);
}

std::tuple<int, int> get_restricted_jobs(int n, int seed){
    std::mt19937 gen(seed);
    std::uniform_int_distribution<int> dist(0, n-1);
    int job1 = dist(gen);
    int job2 = dist(gen);
    while(job1 == job2) job2 = dist(gen);
    return std::make_tuple(job1, job2);
}

// Test function ------------------------------------------------------------------

void test_algorithm(std::vector<int> mus, std::vector<int> ns, std::vector<int> ms, std::vector<double> alphas, int runs, std::string output_file, std::string mutation_string, std::function<std::vector<T>(const std::vector<T>&, std::mt19937&)> mutation_operator, std::string diversity_string){
   
    std::string header = get_csv_line("seed,mu,n,m,alpha,run,generations,max_generations,diversity,fitness,opt,mutation_operator,starting_robustness,ending_robustness,diversity_operator,div_threshold");
    write_to_file(header, output_file, false);
    int max_processing_time = 50;
    std::vector<double> div_thresholds = {0.25, 0.5, 0.75, 0.85, 1};

    auto algorithm_test = [output_file, max_processing_time, mutation_operator, mutation_string, diversity_string, div_thresholds](int mu, int n, int m, float alpha, int run) {

        if(!is_viable_combination(mu, n, m)) return;

        int seed = generate_seed(mu, n, m, alpha, run);
        MachineSchedulingProblem problem = get_problem(seed, n, m, max_processing_time);
        auto [evaluate, diversity_measure_individual, diversity_measure_population] = get_eval_div_funcs(problem, diversity_string, mu, n);
        auto [OPT, optimal_solution] = get_optimal_solution(problem, m, evaluate);
        std::tuple<int, int> restricted_jobs = get_restricted_jobs(n, seed);
        int max_generations = n*n*mu*mu;
        
        auto population = create_population(
            seed, m, n, mu, 
            evaluate, mutation_operator, diversity_measure_individual, diversity_measure_population,
            alpha, optimal_solution
        );

        for(double threshold : div_thresholds){
            auto [starting_robustness, ending_robustness] = run_mu1(
                population,
                terminate_diversitygenerations(threshold, diversity_measure_population, max_generations),
                restricted_jobs
            );
            std::string result = get_csv_line(seed, mu, n, m, alpha, run, population.get_generation(), max_generations, population.get_diversity(diversity_measure_population), population.get_best_fitness(evaluate), OPT, mutation_string, starting_robustness, ending_robustness, diversity_string, threshold);
            write_to_file(result, output_file);
        }

    };

    loop_parameters(mus, ns, ms, alphas, runs, algorithm_test);
}