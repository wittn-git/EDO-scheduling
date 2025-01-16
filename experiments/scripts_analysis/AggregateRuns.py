import sys
import pandas as pd
import os

def aggregate_runs(input_file : str, output_file : str):
    df = pd.read_csv(input_file)
    df = df.drop(columns=['seed', 'run'])
    df = df.groupby(['mu', 'n', 'm', 'alpha', 'mutation_operator', 'diversity_threshold', 'diversity_operator']).agg({'generations': 'mean', 'max_generations': 'mean', 'diversity': 'mean', 'fitness': 'mean', 'opt': 'mean', 'starting_robustness': 'mean', 'ending_robustness': 'mean'}).reset_index()
    df['generation_ratio'] = df['generations'] / df['max_generations']
    df.to_csv(output_file, index=False)

def count_runs(input_file: str, output_file: str, output_folder_stats: str):
    df = pd.read_csv(input_file)
    grouped = df.groupby(["mu", "n", "m", "alpha", "run", "mutation_operator", "diversity_threshold", "diversity_operator", "diversity"])
    mean_robustness = grouped.agg(
        ending_robustness=('ending_robustness', 'mean'),
        starting_robustness=('starting_robustness', 'mean'),
        diversity_score=('diversity', 'mean')
    ).reset_index()
    pivot = mean_robustness.pivot(
        index=["mu", "n", "m", "alpha", "run", "mutation_operator", "diversity_threshold"],
        columns="diversity_operator",
        values=["diversity_score", "diversity_threshold", "ending_robustness", "starting_robustness"]
    )
    diversity_operators = df["diversity_operator"].unique()
    results = []
    
    eucl_miss, sum_miss, both_miss = 0, 0, 0
    for _, row in pivot.iterrows():
        diversity_threshold = row["diversity_threshold"].iloc[0]
        diversity = row["diversity_score"].to_dict()
        if diversity["eucl"] < diversity_threshold and diversity["sum"] < diversity_threshold:
            both_miss += 1
        elif diversity["eucl"] < diversity_threshold:
            eucl_miss += 1
        elif diversity["sum"] < diversity_threshold:
            sum_miss += 1
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
    
    with open(os.path.join(output_folder_stats, "skipped_instances.txt"), "w") as f:
        f.write(f"Both missed threshold: {both_miss}\n")
        f.write(f"Eucl missed threshold: {eucl_miss}\n")
        f.write(f"Sum missed threshold: {sum_miss}\n")
        f.write(f"Total datapoints: {len(results)}\n")
    df_results = pd.DataFrame(results)
    df_results.to_csv(output_file, index=False)
    
if __name__ == "__main__":

    if len(sys.argv) < 5:
        print("Usage: python3 AggregateRuns.py <input_file> <output_agg_file> <output_count_file> <output_folder_stats>")
        exit(1)

    input_file = sys.argv[1]
    output_file_agg, output_file_count, output_folder_stats = sys.argv[2], sys.argv[3], sys.argv[4]

    aggregate_runs(input_file, output_file_agg)
    count_runs(input_file, output_file_count, output_folder_stats)