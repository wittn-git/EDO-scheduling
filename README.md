# PPSN2024-EDO-scheduling

This repository was created for the bachelor thesis of Dominic Wittner with the topic "Evolutionary Diversity Optimization for Machine Scheduling", supervised by Dr. Jakob Bossek (RWTH Chair for AI Methodology).

It now serves as the source code reference and experimental data reference for the paper "Evolutionary Diversity Optimization for Parallel Machine Scheduling" by Dominic Wittner and Jakob Bossek.

## Content of the repository

This repository is mainly divided int two parts. 

The folder "src" contains the C++ source code for the implementation of the used evolutionary algorithm (a class for the population, functions for the used evolutionary operators, a function to run the (µ+1)-EA for a parameter set and a testing function, executing the algorithm for given parameter sets and documenting the results).

The folder experiments is divided in three folders. The "data" folder contains all results of the experiments in csv format. The "scripts_analysis" folder contains the python scripts used to summarize and analyze the results as well as scripts for the generation of tables and plots. The "scripts_execution" folder contains bash scripts to run the experiments with the parameter sets in the paper as well as to run the analysis scripts.

To execute the experiments with the parameter combinations presented in the paper, one simly has to navigate to "experiments/scripts_execution" and execute the bash script "run_experiments.sh". The results will be stored in the "data/runs" folder. Using the the bash script "summarize_results.sh" the results will be concatenated and aggregated in the "data" folder.

If one wishes to execute the experiments with different parameter sets, one can do so by changing the parameter sets in the "run_experiments.sh" script. Alternativly, the "run.sh" in the "experiments/scripts_execution" folder can be used to run the experiments with a single parameter set. In this case, the parameter sets have to be passed as an argument to the script. The parameters are the following:

    - output_file: string                           [path to the output file]
    - Mutation-Operator: {"1RAI", "XRAI"}           [mutation operator used in the EA]
    - Diversity-Operator: {"eucl", "sum", "ord"}    [method of transforming the diversity vector to a scalar]
    - runs: int                                     [number of runs of the EA per parameter set]
    - mus: mu_1,mu_2,...,mu_w (ints)                [population sizes]
    - ns: n_1,n_2,...,n_x (ints)                    [numbers of jobs]
    - ms: m_1,m_2,...m_y (ints)                     [numbers of machines]
    - alphas: a_1,a_2,...,a_z (doubles)             [quality parameters]
    - lambda: double ("-" if unused")               [mean of the poisson distribution for "XRAI"]

They can also be passed directly to the executable, after the code in the "src" folder is complied using CMake.

## TODO (Revision of paper)

- [X] Add the robustness experiments
- [X] Revise the summary of the experiments
- [X] Revise the experiment running code
- [X] Revise the table generation
- [X] Alter DFM definition
- [X] Set table format
- [X] Change proof to: normalized, length optimized
- [X] Add stepwise diversity dependent logging in experiments
- [X] Do preliminary tests for the lambdas of XRAI
- [X] Check if proof is possible for general metrics
- [X] Change paper structure in overleaf
- [X] Consider sorting as alternative method for Euclidean Norm
- [X] Check performance of alternative method
- [X] Write the README.md
- [X] Update the table generation utility
- [X] Alter problem generation by including machine capacities
- [X] Modify seed generation
- [] Find a way to compute the ordering method for larger instances
- [] Run the experiments
- [] Analyze the results
- [] Write the paper
- [] Create file for experimental data