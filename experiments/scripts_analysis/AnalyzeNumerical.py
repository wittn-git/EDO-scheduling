import pandas as pd
import prettytable as pt
import sys
import os

def analyze_numerical(input_file, output_folder):
    df = pd.read_csv(input_file)
    
    column_combinations = [
        ["mu"], ["n"], ["m"], ["alpha"], ["mutation_operator"],
        ["mu", "n"], ["mu", "n", "m"], ["mu", "n", "m", "alpha"], ["mu", "n", "m", "alpha", "mutation_operator"]
    ]
    
    operators = df["diversity_operator"].unique()
    diversity_thresholds = df["diversity_threshold"].unique()
    
    for diversity_threshold in diversity_thresholds:
        df_thresh = df[df["diversity_threshold"] == diversity_threshold]
        output_file = os.path.join(output_folder, f"analysis_{diversity_threshold:.2f}.txt")
        
        with open(output_file, "w") as f:

            f.write("Overall\n")
            table = pt.PrettyTable()
            table.field_names = list(operators) + ["Equal"]
            count_sum, count_eucl, count_eq = 0, 0, 0
            grouped = df_thresh.groupby(["mu", "n", "m", "alpha", "run", "mutation_operator"])
            
            for _, group in grouped:
                rob_eucl = group.loc[group["diversity_operator"] == "eucl", "ending_robustness"].mean()
                rob_sum = group.loc[group["diversity_operator"] == "sum", "ending_robustness"].mean()
                if rob_sum > rob_eucl: count_sum += 1
                elif rob_sum == rob_eucl: count_eq += 1
                else: count_eucl += 1
            
            avg_rob_sum = df_thresh[df_thresh["diversity_operator"] == "sum"]["ending_robustness"].mean() - df_thresh[df_thresh["diversity_operator"] == "sum"]["starting_robustness"].mean()
            avg_rob_eucl = df_thresh[df_thresh["diversity_operator"] == "eucl"]["ending_robustness"].mean() - df_thresh[df_thresh["diversity_operator"] == "eucl"]["starting_robustness"].mean()

            table.add_row([
                f"{count_sum} ({avg_rob_sum:.4f})", 
                f"{count_eucl} ({avg_rob_eucl:.4f})", 
                count_eq
            ])
            f.write(str(table) + "\n\n")
                
            for column_combination in column_combinations:
                f.write(f"Column combination: {column_combination}\n")
                table = pt.PrettyTable()
                table.field_names = ["Values"] + list(operators) + ["Equal"]
                values = df_thresh[column_combination].drop_duplicates()
                for _, value_row in values.iterrows():
                    df_value = df_thresh
                    for col, val in zip(column_combination, value_row):
                        df_value = df_value[df_value[col] == val]
                    grouped = df_value.groupby(["mu", "n", "m", "alpha", "mutation_operator", "run"])
                    count_sum, count_eucl, count_eq = 0, 0, 0
                    for _, group in grouped:
                        rob_eucl = group.loc[group["diversity_operator"] == "eucl", "ending_robustness"].mean()
                        rob_sum = group.loc[group["diversity_operator"] == "sum", "ending_robustness"].mean()
                        if rob_sum > rob_eucl: count_sum += 1
                        elif rob_sum == rob_eucl: count_eq += 1
                        else: count_eucl += 1
                    
                    avg_rob_sum = df_thresh[df_thresh["diversity_operator"] == "sum"]["ending_robustness"].mean() - df_thresh[df_thresh["diversity_operator"] == "sum"]["starting_robustness"].mean()
                    avg_rob_eucl = df_thresh[df_thresh["diversity_operator"] == "eucl"]["ending_robustness"].mean() - df_thresh[df_thresh["diversity_operator"] == "eucl"]["starting_robustness"].mean()

                    table.add_row([
                        str(value_row.values), 
                        f"{count_sum} ({avg_rob_sum:.4f})", 
                        f"{count_eucl} ({avg_rob_eucl:.4f})", 
                        count_eq
                    ])
                
                f.write(str(table) + "\n\n")


if __name__ == "__main__" :

    if len(sys.argv) < 3:
        print("Usage: python3 AnalyzeNumerical.py <input_file_concatenated> <output_folder>")
        exit(1)
    
    input_file = sys.argv[1]
    output_folder = sys.argv[2]

    analyze_numerical(input_file, output_folder)