import matplotlib.pyplot as plt
import pandas as pd
import sys

def plot_trajectory_graph(df, output_folder, file_format, mu, n):

    properties = [("diversity_threshold", "generations"), ("diversity_threshold", "ending_robustness")]
    fig, ax = plt.subplots(1, len(properties), figsize=(10, 5*len(properties)))

    color_map = plt.get_cmap("tab10")
    colors = {val: color_map(i) for i, val in enumerate(df["diversity_operator"].unique())}
    line_styles = ['-', '--', '-.', ':']

    for i, (x, y) in enumerate(properties):

        df_temp = df.groupby(["diversity_operator", "mutation_operator", x])[y].mean().reset_index()
        if i == 0: 
            df_temp = df_temp[df_temp["diversity_threshold"] != 1.0]
        
        for diversity_operator in df["diversity_operator"].unique():
            for j, mutation_operator in enumerate(df["mutation_operator"].unique()):
                df_diversity_operator = df_temp[(df_temp["diversity_operator"] == diversity_operator) & (df_temp["mutation_operator"] == mutation_operator)]
                ax[i].plot(df_diversity_operator[x], df_diversity_operator[y], label=f"{diversity_operator}-{mutation_operator}", color=colors[diversity_operator], linestyle=line_styles[j])
        
        ax[i].set_title(f"{x} vs {y}")
        ax[i].set_xlabel(x)
        ax[i].set_ylabel(y)
        ax[i].legend()

    plt.tight_layout()
    mu_str, n_str = str(mu) if len(mu) > 1 else f"0{mu}", str(n) if len(n) > 1 else f"0{n}"
    plt.savefig(f"{output_folder}/trajectory_graph_mu{mu_str}_n{n_str}.{file_format}")

if __name__ == "__main__":
    if len(sys.argv) < 6:
        print("Usage: python PlotTrajectoryGraph.py <input_file> <output_folder> <file_format> <mu> <n>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_folder = sys.argv[2]
    file_format = sys.argv[3]
    mu = sys.argv[4]
    n = sys.argv[5]

    df = pd.read_csv(input_file)
    plot_trajectory_graph(df, output_folder, file_format, mu, n)