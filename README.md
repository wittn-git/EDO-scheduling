# PPSN2024-EDO-scheduling

This repository was created for the bachelor thesis of Dominic Wittner with the topic "Evolutionary Diversity Optimization for Machine Scheduling", supervised by Dr. Jakob Bossek (RWTH Chair for AI Methodology).

It now serves as the source code reference and experimental data reference for the paper "Evolutionary Diversity Optimization for Parallel Machine Scheduling" by Dominic Wittner and Jakob Bossek.

## TODO (Revision of paper)

- [X] Add the robustness experiments
- [X] Revise the summary of the experiments
- [X] Revise the experiment running code
- [X] Revise the table generation
- [] Alter DFM definition
- [] Run preliminary experiments to get an upper bound on the iterations -> Do we want that? Showing that the euclidean norm is superior only works if the diversity is not maximized
- [] Do preliminary tests for the lambdas of XRAI
- [] Run the experiments
- [] Analyze the results
- [] Write the paper (Proof: Do we want the unnormalized diversity measure for simplicity in the proof or the normalized one for constistency with the experiments?)

### Neccessary Latex packages for tables
\usepackage{array}
\usepackage{booktabs}
\usepackage{multirow}
\usepackage[table]{xcolor}
\usepackage{hhline}
\definecolor{lightgray}{RGB}{211, 211, 211}