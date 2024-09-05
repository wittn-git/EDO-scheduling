# create a function that takes a csv file as input and converts it to a summarized csv file
# seed,mu,n,m,alpha,run,generations,max_generations,diversity,fitness,opt,mutation,starting_robustness,ending_robustness

import sys
import pandas as pd

def summarize_runs(input_file : str, output_file : str):
    df = pd.read_csv(input_file)
    df = df.drop(columns=['seed', 'run'])
    df = df.groupby(['mu', 'n', 'm', 'alpha', 'mutation_operator', 'div_threshold', 'diversity_operator']).agg({'generations': 'mean', 'max_generations': 'mean', 'diversity': 'mean', 'fitness': 'mean', 'opt': 'mean', 'starting_robustness': 'mean', 'ending_robustness': 'mean'}).reset_index()
    df.to_csv(output_file, index=False)

if __name__ == "__main__":

    if len(sys.argv) < 3:
        print("Usage: python3 SummarizeRuns.py <input_file> <output_file>")
        exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    summarize_runs(input_file, output_file)