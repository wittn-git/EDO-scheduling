# PPSN2024-EDO-scheduling

This repository was created for the bachelor thesis of Dominic Wittner with the topic "Evolutionary Diversity Optimization for Machine Scheduling", supervised by Dr. Jakob Bossek (RWTH Chair for AI Methodology).

It now serves as the source code reference and experimental data reference for the paper "Evolutionary Diversity Optimization for Parallel Machine Scheduling" by Dominic Wittner and Jakob Bossek.

## Content of the repository

This repository is mainly divided int two parts. 

The folder "src" contains the C++ source code for the implementation of the used evolutionary algorithm (a class for the population, functions for the used evolutionary operators, a function to run the (µ+1)-EA for a parameter set and a testing function, executing the algorithm for given parameter sets and documenting the results).

The folder experiments is divided in three folders. The "data" folder contains all results of the experiments in csv format. The "scripts_analysis" folder contains the python scripts used to summarize and analyze the results as well as scripts for the generation of tables and plots. The "scripts_execution" folder contains bash scripts to run the experiments with the parameter sets in the paper as well as to run the analysis scripts.

To execute the experiments with the parameter combinations presented in the paper, one simply has to navigate to "experiments/scripts_execution" and execute the bash script "run_experiments.sh". The results will be stored in the "data/runs" folder. Using the bash script "summarize_results.sh" the results will be concatenated and aggregated in the "data" folder.

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

## Requirements

The experiments have been ran on Ubuntu 24.04.1 LTS.
Requirements to use the whole respository (running and analysis of experiments) are:

- g++ 13.2.0
- cmake 3.28.3
- python 3.12.3
- pdflatex 3.141592653-2.6-1.40.25
- bash 5.2.21(1)
- inkscape 1.2.2

In addition, the python packages specified in "experiments/scripts_analysis/requirements.txt" are needed.

## TODO (Revision of paper)

- [x] Add the robustness experiments
- [x] Revise the summary of the experiments
- [x] Revise the experiment running code
- [x] Revise the table generation
- [x] Alter DFM definition
- [x] Set table format
- [x] Change proof to: normalized, length optimized
- [x] Add stepwise diversity dependent logging in experiments
- [x] Do preliminary tests for the lambdas of XRAI
- [x] Check if proof is possible for general metrics
- [x] Change paper structure in overleaf
- [x] Consider sorting as alternative method for Euclidean Norm
- [x] Check performance of alternative method
- [x] Write the README.md
- [x] Update the table generation utility
- [x] Alter problem generation by including machine capacities
- [x] Modify seed generation
- [x] Finish table compile utility
- [x] Find a way to compute the ordering method for larger instances
- [x] Run the experiments
- [x] Write utility to make a trajectory plot for a single parameter set
- [x] Write utility to get a numerical analysis of the results
- [x] Add the plots to the result file
- [x] Numerical analysis: Superiority of operators
- [x] Numerical analysis: Improvement of operators
- [x] Numerical analysis: Overall superiority of operators
- [x] Write count runs
- [x] Write tablerization of count runs in numerical analysis
- [x] Add numerical analysis to the result file
- [x] Fix error in calculation of starting robustness
- [x] Rerun tests
- [x] Think about changes in the experiment parameters: more combinations, changes restriction of parameters
- [] Write the result section of the paper
- [] Write the conclusion of the paper (and future work)
- [] Think about title and keywords of the paper
- [] Format paper and improve language
- [] Beautify the result file