import sys
import pandas as pd
import matplotlib.pyplot as plt

def analyze_numerical(input_file : str, output_folder : str) -> None:
    
    df = pd.read_csv(input_file)
    result = df.groupby(['mutation_operator', 'diversity_operator', 'div_threshold'])['ending_robustness'].sum().reset_index()
    result = result.sort_values(by=['mutation_operator', 'div_threshold', 'diversity_operator'])
    result.to_csv(output_folder + "/result.csv", index=False)

    # plot the data. make one graph for each mutation operator. there, plot div_threshold on x vs ending_robustness on y. one line for each diversity operator
    mutation_operators = result['mutation_operator'].unique()
    for mutation_operator in mutation_operators:
        data = result[result['mutation_operator'] == mutation_operator]
        diversity_operators = data['diversity_operator'].unique()
        for diversity_operator in diversity_operators:
            data_div = data[data['diversity_operator'] == diversity_operator]
            plt.plot(data_div['div_threshold'], data_div['ending_robustness'], label=diversity_operator)
        plt.xlabel('div_threshold')
        plt.ylabel('ending_robustness')
        plt.title(mutation_operator)
        plt.legend()
        plt.savefig(output_folder + "/" + mutation_operator + ".png")
        plt.close()

if __name__ == "__main__" :

    if len(sys.argv) < 3:
        print("Usage: python3 AnalyzeNumerical.py <input_file> <output_folder>")
        exit(1)
    
    input_file, output_folder = sys.argv[1], sys.argv[2]

    analyze_numerical(input_file, output_folder)