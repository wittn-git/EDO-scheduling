import sys
import pandas as pd
import time

def aggregate_runs(input_file : str, output_file : str):
    df = pd.read_csv(input_file)
    df = df.drop(columns=['seed', 'run'])
    df = df.groupby(['mu', 'n', 'm', 'alpha', 'mutation_operator', 'diversity_threshold', 'diversity_operator']).agg({'generations': 'mean', 'max_generations': 'mean', 'diversity': 'mean', 'fitness': 'mean', 'opt': 'mean', 'starting_robustness': 'mean', 'ending_robustness': 'mean'}).reset_index()
    df['generation_ratio'] = df['generations'] / df['max_generations']
    df.to_csv(output_file, index=False)

def count_runs(input_file: str, output_file: str):
    df = pd.read_csv(input_file)
    grouped = df.groupby(["mu", "n", "m", "alpha", "run", "mutation_operator", "diversity_threshold", "diversity_operator"])
    mean_robustness = grouped.agg(
        ending_robustness=('ending_robustness', 'mean'),
        starting_robustness=('starting_robustness', 'mean')
    ).reset_index()
    pivot = mean_robustness.pivot(
        index=["mu", "n", "m", "alpha", "run", "mutation_operator", "diversity_threshold"],
        columns="diversity_operator",
        values=["ending_robustness", "starting_robustness"]
    )
    diversity_operators = df["diversity_operator"].unique()
    results = []
    
    for _, row in pivot.iterrows():
        # TODO improvements are not calculated correctly
        starting_values, ending_values = row["starting_robustness"].to_dict(), row["ending_robustness"].to_dict()        
        improvements = {f"{op}_improvement": ending_values[op] - starting_values[op] for op in diversity_operators}
        max_robustness = max(ending_values.values())
        superior_operator = (
            [op for op, val in ending_values.items() if val == max_robustness]
            if list(ending_values.values()).count(max_robustness) == 1 else ["equal"]
        )[0]
        result_row = dict(zip(pivot.index.names, row.name))
        result_row["superior_op"] = superior_operator
        result_row.update(improvements)
        results.append(result_row)
    
    df_results = pd.DataFrame(results)
    df_results.to_csv(output_file, index=False)
    
if __name__ == "__main__":

    if len(sys.argv) < 4:
        print("Usage: python3 AggregateRuns.py <input_file> <output_agg_file> <output_count_file>")
        exit(1)

    input_file = sys.argv[1]
    output_file_agg, output_file_count = sys.argv[2], sys.argv[3]

    aggregate_runs(input_file, output_file_agg)
    count_runs(input_file, output_file_count)
    