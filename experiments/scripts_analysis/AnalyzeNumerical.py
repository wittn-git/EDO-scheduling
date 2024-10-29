import pandas as pd
from collections import Counter
import prettytable as pt
import sys

# TODO Analyze the following three aspects: generations, how many which operator had the best robustness, what as the average improvement of the best operator
def analyze_numerical(input_file_con, input_file_agg, output_folder):
    
    df = pd.read_csv(input_file_con)
    column_combinations = [
        ["mu"], ["n"], ["m"], ["alpha"], ["mutation_operator"],
        ["mu", "n"], ["mu", "n", "m"], ["mu", "n", "m", "alpha"]
    ]
    operators = df["diversity_operator"].unique()
    diversity_thresholds = df["diversity_threshold"].unique()
    
    with open(output_folder + "/output.txt", 'w') as f:

        f.write("Overall\n")
        table = pt.PrettyTable()
        table.field_names = ["Div thresh."] + list(operators)
        for div_thresh in diversity_thresholds:
            df_thresh = df[df["diversity_threshold"] == div_thresh]
            best_operator_counts = {op: 0 for op in operators}
            grouped = df_thresh.groupby(["mu", "n", "m", "alpha", "run"])
            
            for _, group in grouped:
                max_robustness = group["ending_robustness"].max()
                best_operators = group[group["ending_robustness"] == max_robustness]["diversity_operator"]
                for best_operator in best_operators:
                    best_operator_counts[best_operator] += 1
            table.add_row([div_thresh] + [best_operator_counts[op] for op in operators])
        f.write(str(table) + "\n\n")
        '''
        for column_combination in column_combinations:
            f.write("Column combination: " + str(column_combination) + "\n")
            table = pt.PrettyTable()
            table.field_names = ["Values"] + list(operators)
            
            # get each unique value of the column combination
            values = df[column_combination].drop_duplicates()

            f.write(str(table) + "\n\n")
        '''

if __name__ == "__main__" :

    if len(sys.argv) < 4:
        print("Usage: python3 AnalyzeNumerical.py <input_file_concatenated> <input_file_aggregated> <output_folder>")
        exit(1)
    
    input_file_con, input_file_agg = sys.argv[1], sys.argv[2]
    output_folder = sys.argv[3]

    analyze_numerical(input_file_con, input_file_agg, output_folder)