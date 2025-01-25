import sys
import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

def plot_generations(input_file_count, output_folder, file_extension):
    df = pd.read_csv(input_file_count)
    df = df[df["diversity_threshold"] == 1]
    column_combinations = [["mu"], ["n"], ["m"], ["alpha"]]
    column_combination_mapping = {
        "mu": "Population Size", 
        "n": "Number of Jobs", 
        "m": "Number of Machines", 
        "alpha": "Quality Parameter", 
        "mutation_operator": "Mutation Operator"
    }
    plt.rcParams.update({'font.size': 22})
    fig, axes = plt.subplots(ncols=4, nrows=1, figsize=(24, 6))
    axes = axes.flatten()

    for index, column_combination in enumerate(column_combinations):
        ax = axes[index]
        title = ", ".join([column_combination_mapping[col] for col in column_combination])
        ax.set_title(title)

        values = df[column_combination].drop_duplicates().values
        values_n = len(values)
        xticks = []
        xtick_labels = []

        for i, value_row in enumerate(values):
            df_value = df
            for col, val in zip(column_combination, value_row):
                df_value = df_value[df_value[col] == val]

            pos_start = i * 2  # Start position for this set of boxplots
            for j, div_op in enumerate(df_value["diversity_operator"].unique()):
                df_div_op = df_value[df_value["diversity_operator"] == div_op]
                hatch = "" if div_op == "eucl" else "//"
                ax.boxplot(
                    df_div_op["generation_ratio"], 
                    positions=[pos_start + j * 0.5], 
                    widths=0.4, 
                    patch_artist=True, 
                    boxprops=dict(facecolor="white", hatch=hatch), 
                    medianprops=dict(color="black", linewidth=1)
                )

            # Center tick between the two boxplots
            mid_pos = pos_start + 0.25
            xticks.append(mid_pos)
            xtick_labels.append(", ".join(map(str, value_row)))

        ax.set_xticks(xticks)
        ax.set_xticklabels(xtick_labels, ha="center")

        if index == 0: 
            ax.set_ylabel("Generation Ratio")
        else:
            ax.set_yticks([])

    # Add a legend for all subplots
    legend_elements = [
        Patch(facecolor="white", hatch="", label=r'$||\cdot||_2$', edgecolor="black"),
        Patch(facecolor="white", hatch="//", label=r'$\sum \cdot$', edgecolor="black")        
    ]
    fig.legend(handles=legend_elements, loc="lower center", ncol=2, bbox_to_anchor=(0.5, -0.1))

    output_file = os.path.join(output_folder, f"generationplot.{file_extension}")
    fig.tight_layout(rect=[0, 0, 1, 0.95])  # Adjust layout to make space for the legend
    fig.savefig(output_file, bbox_inches='tight')

if __name__ == "__main__" :
    if len(sys.argv) < 4:
        print("Usage: python3 PlotGenerations.py <input_file_agg> <output_folder> <file_extension>")
        exit(1)
    
    input_file_agg = sys.argv[1]
    output_folder = sys.argv[2]
    file_extension = sys.argv[3]

    plot_generations(input_file_agg, output_folder, file_extension)
