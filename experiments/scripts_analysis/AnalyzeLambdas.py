import sys
import pandas as pd

# preliminary experiments for lambdas
# lambdas=("0" "0.1" "0.15" "0.2" "0.4" "0.75" "1" "1.2" "1.5" "2" "2.5" "3")
# mus="2,3,5,8"
# ns="5,7,10"
# ms="1,3"
# runs="10"
# alphas="0.3,0.6,1"

def analyze_lambdas(input_file : str, euclidean_norm : int):
    
    categories = [("diversity", "max"), ("ending_robustness", "max"), ("fitness", "max"), ("generations", "min")]
    analysis_results = {}

    df = pd.read_csv(input_file)
    df = df[df["euclidean_norm"] == euclidean_norm]
    grouped = df.groupby(['mu', 'n', 'm', 'alpha'])
    mutations = df["mutation"].unique()

    for category, best in categories:
        category_results = {mutation: 0 for mutation in mutations}
        for name, group in grouped:
            best_value = group[category].min() if best == "min" else group[category].max()
            best_mutations = group[group[category] == best_value]["mutation"].unique()
            for mutation in best_mutations:
                category_results[mutation] += 1
        analysis_results[category] = category_results

    ranks = {mutation: 0 for mutation in mutations}
    for category in analysis_results:
        sorted_mutations = sorted(analysis_results[category].items(), key=lambda x: x[1], reverse=True)
        for i, (mutation, count) in enumerate(sorted_mutations):
            ranks[mutation] += i

    sorted_ranks = sorted(ranks.items(), key=lambda x: x[1])
    print("\nRanks")
    for mutation, rank in sorted_ranks:
        print(f"{mutation}: {rank}")

if __name__ == "__main__":

    if len(sys.argv) < 3:
        print("Usage: python3 AnalyzeLambdas.py <input_file> <euclidean_norm>")
        exit(1)

    input_file = sys.argv[1]
    euclidean_norm = int(sys.argv[2])

    analyze_lambdas(input_file, euclidean_norm)