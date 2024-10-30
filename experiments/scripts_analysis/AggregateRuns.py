import sys
import pandas as pd
import time

def aggregate_runs(input_file : str, output_file : str):
    df = pd.read_csv(input_file)
    df = df.drop(columns=['seed', 'run'])
    df = df.groupby(['mu', 'n', 'm', 'alpha', 'mutation_operator', 'diversity_threshold', 'diversity_operator']).agg({'generations': 'mean', 'max_generations': 'mean', 'diversity': 'mean', 'fitness': 'mean', 'opt': 'mean', 'starting_robustness': 'mean', 'ending_robustness': 'mean'}).reset_index()
    df['generation_ratio'] = df['generations'] / df['max_generations']
    df.to_csv(output_file, index=False)

def count_runs(input_file : str, output_file : str):
    df = pd.read_csv(input_file)
    grouped = df.groupby(["mu", "n", "m", "alpha", "run", "mutation_operator", "diversity_threshold"])
    diversity_operators = df["diversity_operator"].unique()
    cols = ["mu", "n", "m", "alpha", "mutation_operator", "run", "diversity_threshold", "superior_op"] + [f"{op}_improvement" for op in diversity_operators]
    df_results = pd.DataFrame(columns=cols)
    for _, group in grouped:
        robustness = {op: group.loc[group["diversity_operator"] == op, "ending_robustness"].mean() for op in diversity_operators}
        superior_operator = max(robustness, key=robustness.get) if len(set(robustness.values())) == len(robustness) else "equal"
        improvements = {f"{op}_improvement": robustness[op] - group.loc[group["diversity_operator"] == op, "starting_robustness"].mean() for op in diversity_operators}
        row = group.iloc[0][["mu", "n", "m", "alpha", "mutation_operator", "run", "diversity_threshold"]].to_dict()
        row["superior_op"] = superior_operator
        row.update(improvements)
        df_results = pd.concat([df_results, pd.DataFrame([row])])
    df_results.to_csv(output_file, index=False)
    
if __name__ == "__main__":

    if len(sys.argv) < 4:
        print("Usage: python3 AggregateRuns.py <input_file> <output_agg_file> <output_count_file>")
        exit(1)

    input_file = sys.argv[1]
    output_file_agg, output_file_count = sys.argv[2], sys.argv[3]

    aggregate_runs(input_file, output_file_agg)
    count_runs(input_file, output_file_count)