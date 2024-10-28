import pandas as pd
from itertools import chain, combinations
from collections import Counter
import prettytable as pt
import sys

def analyze_numerical(input_file_con, input_file_agg, output_folder):
    # Load the data
    df = pd.read_csv(input_file_con)

    # Define columns and get all combinations
    # TODO get over
    # TODO summarize better and only take more speficic columns
    columns = ['mu', 'n', 'm', 'alpha', 'mutation_operator']
    column_combinations = chain.from_iterable(combinations(columns, r) for r in range(1, len(columns)+1))  # Exclude empty combination
    operators = df["diversity_operator"].unique()
    
    with open(output_folder + "/output.txt", 'w') as f:
        # Iterate over each column combination
        for column_combination in column_combinations:
            f.write("Column combination: " + str(column_combination) + "\n")
            table = pt.PrettyTable()
            table.field_names = ["Values"] + list(operators)
            
            # Group by the current column combination
            grouped = df.groupby(list(column_combination))
            
            # For each group, count the diversity operator with highest robustness
            for values, group in grouped:
                # Check for highest robustness per seed
                max_counts = Counter()
                
                for seed, seed_group in group.groupby('seed'):
                    max_robustness = seed_group['ending_robustness'].max()
                    top_operators = seed_group[seed_group['ending_robustness'] == max_robustness]['diversity_operator'].values
                    max_counts.update(top_operators)
                
                # Prepare table row
                row = [values] + [max_counts.get(op, 0) for op in operators]
                table.add_row(row)
            
            # Write the table to the output file
            f.write(str(table) + "\n\n")

if __name__ == "__main__" :

    if len(sys.argv) < 4:
        print("Usage: python3 AnalyzeNumerical.py <input_file_concatenated> <input_file_aggregated> <output_folder>")
        exit(1)
    
    input_file_con, input_file_agg = sys.argv[1], sys.argv[2]
    output_folder = sys.argv[3]

    analyze_numerical(input_file_con, input_file_agg, output_folder)