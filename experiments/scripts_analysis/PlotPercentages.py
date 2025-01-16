import sys
import os
import pandas as pd
import matplotlib.pyplot as plt

def plot_percentages(input_file_count, output_folder_plots, output_folder_stats, file_extension):
    df = pd.read_csv(input_file_count)
    op_mapping = {"eucl": "$||\\cdot||$", "sum": "$\\sum \\cdot$"}

    statistics_file = os.path.join(output_folder_stats, f"percentage_both_statistics.txt")
    with open(statistics_file, "w") as f:
        f.write("")

    plt.figure(figsize=(12, 6))
    plt.rcParams.update({'font.size': 22})
    line_styles = ["-", "--"]
    diversity_thresholds = df["diversity_threshold"].unique()

    for i, op in enumerate(["eucl", "sum"]):
        X = []
        for div_thresh in diversity_thresholds:
            df_thresh = df[df["diversity_threshold"] == div_thresh]
            X.append(df_thresh[f"{op}_improvement"].mean()*100)
        plt.plot(diversity_thresholds, X, label=op_mapping[op], linestyle=line_styles[i], color='black', linewidth=2)
        with open(statistics_file, "a") as f:
            f.write(f"{op}: {[round(x, 4) for x in X]}\n")

    plt.xlabel("Diversity")
    plt.ylabel("Improvement (%)")
    plt.legend()
    plt.tight_layout()
    
    output_file = os.path.join(output_folder_plots, f"percentageplot.{file_extension}")
    plt.savefig(output_file, bbox_inches='tight')

if __name__ == "__main__" :

    if len(sys.argv) < 5:
        print("Usage: python3 PlotPercentages.py <input_file_count> <output_folder_plots> <output_folder_stats> <file_extension>")
        exit(1)
    
    input_file_count = sys.argv[1]
    output_folder_plots, output_folder_stats = sys.argv[2], sys.argv[3]
    file_extension = sys.argv[4]

    plot_percentages(input_file_count, output_folder_plots, output_folder_stats, file_extension)