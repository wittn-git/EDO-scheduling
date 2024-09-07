import sys
import matplotlib.pyplot as plt

def get_balanced_vector(vec_size, max_sim, count):
    base_value = count // vec_size
    remainder = count % vec_size
    return [min(max_sim, base_value + (1 if i < remainder else 0)) for i in range(vec_size)]


def get_unbalanced_vector(vec_size, max_sim, count):
    full_index = int(count // max_sim)
    vector = [max_sim] * full_index + [count % max_sim] + [0] * (vec_size - full_index - 1)
    return vector

def get_div_fun(p, vec_size, max_sim):
    max_value = sum([x**p for x in [max_sim]*vec_size])**(1/p)
    print(max_value)
    def div_fun(vec):
        return 1 - (sum([x**p for x in vec])**(1/p)) / max_value
    return div_fun

def generate_plot(output_file, mu, max_sim, p):
    vec_size = int((mu*(mu-1))/2)
    max_count = int(max_sim * vec_size)
    div_fun = get_div_fun(p, vec_size, max_sim)

    X = [i for i in range(1, max_count+1)]
    Y_balanced = [div_fun(get_balanced_vector(vec_size, max_sim, count)) for count in X]
    Y_unbalanced = [div_fun(get_unbalanced_vector(vec_size, max_sim, count)) for count in X]

    plt.figure(figsize=(12, 6))
    plt.rcParams.update({'font.size': 22})
    plt.plot(X, Y_balanced, label="$D$ maximing b", linestyle="--", color='black', linewidth=2)
    plt.plot(X, Y_unbalanced, label="$D$ minimizing b", linestyle="-", color='black', linewidth=2)
    plt.xlabel("S($D$)")
    plt.ylabel(f"div(P)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_file)

if __name__ == "__main__" :
    if len(sys.argv) < 5:
        # mu : population size, max_sim : maximum similarity of two individuals, p : used l^p norm
        print("Usage: python3 PlotClusterExample.py <output_file> <mu> <max_sim> <p>")
        exit(1)
    
    output_file = sys.argv[1]
    mu = int(sys.argv[2])
    max_sim = float(sys.argv[3])
    p = int(sys.argv[4])

    generate_plot(output_file, mu, max_sim, p)