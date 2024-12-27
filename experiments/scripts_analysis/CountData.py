import sys
import pandas as pd
import itertools

def check_missing(concat_input_file : str):
    
    df = pd.read_csv(concat_input_file)

    mutation_operators, diversity_operators = df['mutation_operator'].unique(), df['diversity_operator'].unique()
    operator_pairs = [(mut_op, div_op) for mut_op in mutation_operators for div_op in diversity_operators]

    mus = [2, 5, 10, 25]
    ns = [5, 10, 15, 25, 50]
    ms = [1, 3, 5]
    alphas = [0.3, 0.6, 1]
    parameter_combinations = itertools.product(mus, ns, ms, alphas)

    runs = 50
    diversity_threshold_n = len([i / 100 for i in range(0, 101, 5)])
    datapoints_n = runs * diversity_threshold_n

    points_missing, points_overall = 0, 0
    print("Checking for missing data points:")
    for mut_op, div_op in operator_pairs:
        print(f"Operators: {mut_op}, {div_op}")

        for mu, n, m, alpha in parameter_combinations:
            if not((m < n) and (mu <= n/m)):
                continue
            df_filtered = df[(df['mu'] == mu) & (df['n'] == n) & (df['m'] == m) & (df['alpha'] == alpha) & (df['mutation_operator'] == mut_op) & (df['diversity_operator'] == div_op)]
            current_points_n = len(df_filtered)
            points_overall += current_points_n
            if current_points_n != datapoints_n:
                points_missing += datapoints_n - current_points_n
                print(f"mu: {mu}, n: {n}, m: {m}, alpha: {alpha}: {current_points_n} / {datapoints_n}")
    
    print(f"\nTotal points overall: {points_overall}")
    print(f"Total points missing: {points_missing}")

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Usage: python3 CountData.py <concat_input_file>")
        exit(1)

    concat_input_file = sys.argv[1]

    check_missing(concat_input_file)