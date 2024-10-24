import sys
import pandas as pd
import matplotlib.pyplot as plt

def plot_trajectory_graph(input_file, output_folder, mu, n, m, alpha, mutation_operator):
    
    df = pd.read_csv(input_file)
    df = df[(df["mu"] == mu) & (df["n"] == n) & (df["m"] == m) & (df["alpha"] == alpha) & (df["mutation_operator"] == mutation_operator)]

    if df.empty:
        return

    properties = [("generations", "diversity"), ("diversity", "ending_robustness")]
    fig, ax = plt.subplots(1, len(properties), figsize=(10, 5*len(properties)))

    for i, (x, y) in enumerate(properties):
        for diversity_operator in df["diversity_operator"].unique():
            df_diversity_operator = df[df["diversity_operator"] == diversity_operator]
            ax[i].plot(df_diversity_operator[x], df_diversity_operator[y], label=diversity_operator)
        
        ax[i].set_title(f"{x} vs {y}")
        ax[i].set_xlabel(x)
        ax[i].set_ylabel(y)
        ax[i].legend()

    plt.savefig(f"{output_folder}/trajectory_graph_{mu}_{n}_{m}_{alpha}_{mutation_operator}.png")

if __name__ == "__main__" :

    if len(sys.argv) < 8:
        print("Usage: python3 PlotTrajectoryGraph.py <input_file> <output_folder> <mu> <n> <m> <alpha> <operator>")
        exit(1)
    
    input_file, output_folder = sys.argv[1], sys.argv[2]
    mu, n, m, alpha = int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), float(sys.argv[6])
    mutation_operator = sys.argv[7]

    plot_trajectory_graph(input_file, output_folder, mu, n, m, alpha, mutation_operator)