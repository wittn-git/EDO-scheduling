import sys
import os
import pandas as pd
import matplotlib.pyplot as plt

def plot_percentages(input_file_count, output_folder_plots, output_folder_stats, file_extension):

    statistics_files = os.path.join(output_folder_stats, f"percentage_eucl_statistics.txt")

    df = pd.read_csv(input_file_count)
    column_combinations = [
        ["mu"], ["n"], ["m"], ["alpha"], ["mutation_operator"]
    ]
    column_combination_mapping = {
        "mu": "Population Size", "n": "Number of Jobs", "m": "Number of Machines", "alpha": "Quality Parameter", "mutation_operator": "Mutation Operator"
    }
    value_mapping ={
        "XRAI_0.10": "X(R+I), $\\lambda=0.1$", "XRAI_1.00": "X(R+I), $\\lambda=1$", "XRAI_1.50": "X(R+I), $\\lambda=1.5$", "1RAI": "1(R+I)"
    }
    
    diversity_thresholds = df["diversity_threshold"].unique()

    line_style_names = {
        'solid':                (0, ()),
        'dotted':               (0, (1, 5)),
        'densely dotted':       (0, (1, 1)),
        'dashed':               (0, (5, 5)),
        'dashdotted':           (0, (3, 5, 1, 5)),
        'dashdotdotted':        (0, (3, 5, 1, 5, 1, 5))
    }
    line_styles = list(line_style_names.values())

    plt.rcParams.update({'font.size': 22})
    X_values = []
    plt.tight_layout()
    fig, axes = plt.subplots(ncols=3, nrows=2, figsize=(24, 16))
    fig.subplots_adjust(hspace=0.1)
    axes = axes.flatten()
    axes[0].set_title("Overall")
    
    overall_X = []
    for diversity_threshold in diversity_thresholds:
        df_thresh = df[(df["diversity_threshold"] == diversity_threshold)]
        improvement = df_thresh["eucl_improvement"].mean() 
        overall_X.append(improvement*100)    
    with open(statistics_files, "w") as f:
        f.write(f"Overall: {[round(x, 4) for x in overall_X]}\n")
    axes[0].plot(diversity_thresholds, overall_X, linestyle=line_styles[0], color="black")
    X_values.extend(overall_X)

    for index, column_combination in enumerate(column_combinations):
        
        ax = axes[index+1]
        title = ", ".join([column_combination_mapping[col] for col in column_combination])
        ax.set_title(title)

        values = df[column_combination].drop_duplicates().values
        for i, value_row in enumerate(values):
            df_value = df
            for col, val in zip(column_combination, value_row):
                df_value = df_value[df_value[col] == val]
            X = []
            for diversity_threshold in diversity_thresholds:
                df_thresh = df_value[(df_value["diversity_threshold"] == diversity_threshold)]
                improvement = df_thresh["eucl_improvement"].mean() 
                X.append(improvement*100)    
            with open(statistics_files, "a") as f:
                f.write(f"{column_combination} -> {value_row}: {[round(x, 4) for x in X]}\n")
            X_values.extend(X)
            label = str(value_row).replace("[", "").replace("]", "").replace("'", "")  
            label = value_mapping[label] if label in value_mapping else label
            ax.plot(diversity_thresholds, X, label=label, linestyle=line_styles[i], color="black")
    
    for i, ax in enumerate(axes):
        if i != 0: ax.legend()
        ax.axhline(y=0, color='black')
        if i > 2:   
            ax.set_xlabel("Diversity")
            ax.set_xticks([i/100 for i in range(0, 101, 20)])
        else:
            ax.set_xticks([])
        if i % 3 == 0:
            ax.set_ylabel("Improvement (%)")
        else:
            ax.set_yticks([])
        min_val, max_val = min(X_values)*1.1, max(X_values)*1.1
        ax.set_ylim([min_val, max_val])
    
    output_file = os.path.join(output_folder_plots, f"percentageplot_sixfold.{file_extension}")
    fig.savefig(output_file, bbox_inches='tight')

if __name__ == "__main__" :

    if len(sys.argv) < 4:
        print("Usage: python3 PlotPercentagesSixfold.py <input_file_count> <output_folder_plots> <output_folder_stats> <file_extension>")
        exit(1)
    
    input_file_count = sys.argv[1]
    output_folder_plots, output_folder_stats = sys.argv[2], sys.argv[3]
    file_extension = sys.argv[4]

    plot_percentages(input_file_count, output_folder_plots, output_folder_stats, file_extension)