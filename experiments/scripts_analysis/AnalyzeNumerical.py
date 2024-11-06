import pandas as pd
import prettytable as pt
import sys
import os

def analyze_numerical(input_file_count, input_file_agg, output_folder):

    df = pd.read_csv(input_file_count)
    column_combinations = [
        ["mu"], ["n"], ["m"], ["alpha"], ["mutation_operator"],
        ["mu", "n"], ["mu", "n", "m"], ["mu", "n", "m", "alpha"], ["mu", "n", "m", "alpha", "mutation_operator"]
    ]
    
    df_agg = pd.read_csv(input_file_agg)
    diversity_operators = list(df_agg["diversity_operator"].unique()) + ["equal"]
    diversity_thresholds = df["diversity_threshold"].unique()
    
    for diversity_threshold in diversity_thresholds:
        df_thresh = df[df["diversity_threshold"] == diversity_threshold]
        output_file = os.path.join(output_folder, f"analysis_{diversity_threshold:.2f}.txt")
        with open(output_file, "w") as f:

            f.write("Overall\n")
            table = pt.PrettyTable()
            table.field_names = list(diversity_operators)
            row = []
            for op in diversity_operators:
                count = df_thresh[df_thresh["superior_op"] == op].shape[0]
                if op != "equal": 
                    count = (count, round(df_thresh[f"{op}_improvement"].mean(), 5))
                row.append(count)
            table.add_row(row)
            f.write(str(table) + "\n\n")
                
            for column_combination in column_combinations:
                f.write(f"Column combination: {column_combination}\n")
                table = pt.PrettyTable()
                table.field_names = ["Values"] + list(diversity_operators)
                values = df_thresh[column_combination].drop_duplicates().values
                for value_row in values:
                    df_value = df_thresh
                    for col, val in zip(column_combination, value_row):
                        df_value = df_value[df_value[col] == val]
                    row = [value_row] 
                    for op in diversity_operators:
                        count = df_value[df_value["superior_op"] == op].shape[0]
                        if op != "equal":
                            count = (count, df_thresh[f"{op}_improvement"].mean())
                        row.append(count)
                    table.add_row(row)
                
                f.write(str(table) + "\n\n")


if __name__ == "__main__" :

    if len(sys.argv) < 4:
        print("Usage: python3 AnalyzeNumerical.py <input_file_count> <input_file_agg> <output_folder>")
        exit(1)
    
    input_file_count, input_file_agg = sys.argv[1], sys.argv[2]
    output_folder = sys.argv[3]

    analyze_numerical(input_file_count, input_file_agg, output_folder)