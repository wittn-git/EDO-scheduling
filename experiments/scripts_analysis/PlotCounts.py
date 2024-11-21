import sys
import os
import pandas as pd
import matplotlib.pyplot as plt

def plot_counts(input_file_count, input_file_agg, output_folder, file_extension):

    df = pd.read_csv(input_file_count)
    column_combinations = [
        ["mu"], ["n"], ["m"], ["alpha"], ["mutation_operator"]
    ]
    
    df_agg = pd.read_csv(input_file_agg)
    diversity_operators = list(df_agg["diversity_operator"].unique())
    diversity_thresholds = df["diversity_threshold"].unique()

    color_map = plt.get_cmap("tab10")
    colors = {val: color_map(i) for i, val in enumerate(diversity_operators)}
    line_styles = ["-", "--", "-.", ":"]
                
    for column_combination in column_combinations:
        
        plt.figure()
        values = df[column_combination].drop_duplicates().values
        for i, value_row in enumerate(values):
            df_value = df
            for col, val in zip(column_combination, value_row):
                df_value = df_value[df_value[col] == val]
            for op in diversity_operators:
                X = []
                for diversity_threshold in diversity_thresholds:
                    X.append(df_value[(df_value["superior_op"] == op) & (df_value["diversity_threshold"] == diversity_threshold)].shape[0])
                plt.plot(diversity_thresholds, X, label=f"{op}_{value_row}", linestyle=line_styles[i%len(line_styles)], color=colors[op])
        
        plt.legend()
        output_file = os.path.join(output_folder, f"countplot_{"_".join(column_combination)}.{file_extension}")
        plt.savefig(output_file)
        plt.close()

if __name__ == "__main__" :

    if len(sys.argv) < 5:
        print("Usage: python3 PlotCounts.py <input_file_count> <input_file_agg> <output_folder> <file_extension>")
        exit(1)
    
    input_file_count, input_file_agg = sys.argv[1], sys.argv[2]
    output_folder = sys.argv[3]
    file_extension = sys.argv[4]

    plot_counts(input_file_count, input_file_agg, output_folder, file_extension)