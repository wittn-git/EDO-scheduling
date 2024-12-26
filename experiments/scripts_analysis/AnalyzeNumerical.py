import pandas as pd
import sys
import os

def wrap_table(table, font_name):
    result = "\\begin{center}\n\\renewcommand{\\tabcolsep}{4pt}\n\\renewcommand{\\arraystretch}{1.1}\n"
    result += f"\\begin{{{font_name}}}\n"
    result += table
    result += f"\\end{{{font_name}}}\n" + "\\end{center}\n"
    return result

def get_legend_row(n_col):
    result = "\\multicolumn{"+str(n_col)+"}{l}{\\#Sup: Instances with superior robustness} \\\\ \n"
    result += "\\multicolumn{"+str(n_col)+"}{l}{$\\uparrow$: Average improvement of robustness.} \\\\ \n"
    result += "\\multicolumn{"+str(n_col)+"}{l}{\\#: Count of instances.} \\\\ \n"
    return result

def analyze_numerical(input_file_count, input_file_agg, output_folder):

    df = pd.read_csv(input_file_count)
    column_combinations = [
        ["mu"], ["n"], ["m"], ["alpha"], ["mutation_operator"]
    ]
    operator_mapping = {
        "eucl": "$\\lVert \\cdot \\rVert_2$",
        "sum": "$\\Sigma \\cdot$",
        "equal": "Equal"
    }
    column_combination_mapping = {
        "mu": "Population Size", "n": "Number of Jobs", "m": "Number of Machines", "alpha": "Quality Parameter", "mutation_operator": "Mutation Operator"
    }
    value_mapping ={
        "XRAI_0.10": "X(R+I), $\\lambda=0.1$", "XRAI_1.00": "X(R+I), $\\lambda=1$", "XRAI_1.50": "X(R+I), $\\lambda=1.5$", "1RAI": "1(R+I)"
    }
    
    df_agg = pd.read_csv(input_file_agg)
    diversity_operators = list(df_agg["diversity_operator"].unique()) + ["equal"]
    diversity_thresholds = df["diversity_threshold"].unique()
    
    for diversity_threshold in diversity_thresholds:
        df_thresh = df[df["diversity_threshold"] == diversity_threshold]
        output_file = os.path.join(output_folder, f"table_numerical_div[{diversity_threshold:.2f}].tex")
        with open(output_file, "w") as f:
            f.write("Overall\n")
            table = "\\begin{tabular}{rrrrr}\n\\toprule\n"
            multicolumns = []
            for i, op in enumerate(diversity_operators):
                cols = 1 if op == "equal" else 2
                multicolumns.append(f"\\multicolumn{{{cols}}}{{c}}{{{operator_mapping[op]}}}")
            table += " & ".join(multicolumns) + " \\\\ \n"
            table += "\\cmidrule(lr){1-2} \\cmidrule(lr){3-4}  \\cmidrule(lr){5-5}\n"           
            table += " & ".join(["\\#Sup", "$\\uparrow$", "\\#Sup", "$\\uparrow$", "\\#"]) + " \\\\ \n"
            table += "\\midrule\n"
            for op in diversity_operators:
                count = df_thresh[df_thresh["superior_op"] == op].shape[0]
                table += str(count)
                if op != "equal": 
                    improvement = f"{float(df_thresh[f"{op}_improvement"].mean()):.5f}"
                    table += f" & {improvement} & "
                else:
                    table += " \\\\ \n"
            table += "\\bottomrule\n"
            table += get_legend_row(5)
            table += "\\end{tabular}\n\n"


            f.write(wrap_table(str(table), "customsize"))
            f.write("\n\n")
  
            for column_combination in column_combinations:
                comb_str = "_".join(column_combination)
                comb_str = column_combination_mapping[comb_str] if comb_str in column_combination_mapping else comb_str
                f.write(f"{comb_str}\n")
                table = "\\begin{tabular}{lrrrrr}\n\\toprule\n"
                multicolumns = ["\\multicolumn{1}{c}{Values}"]
                for i, op in enumerate(diversity_operators):
                    cols = 1 if op == "equal" else 2
                    multicolumns.append(f"\\multicolumn{{{cols}}}{{c}}{{{operator_mapping[op]}}}")
                table += " & ".join(multicolumns) + " \\\\ \n"
                table += "\\cmidrule(lr){2-3} \\cmidrule(lr){4-5}  \\cmidrule(lr){6-6}\n"           
                table += " & ".join(["", "\\#Sup", "$\\uparrow$", "\\#Sup", "$\\uparrow$", "\\#"]) + " \\\\ \n"
                table += "\\midrule\n"
                values = df_thresh[column_combination].drop_duplicates().values
                for value_row in values:
                    df_value = df_thresh
                    for col, val in zip(column_combination, value_row):
                        df_value = df_value[df_value[col] == val]
                    val_str = str(value_row).replace("[", "").replace("]", "").replace("'", "")
                    val_str = value_mapping[val_str] if val_str in value_mapping else val_str
                    table += f"{val_str} & "
                    for op in diversity_operators:
                        count = df_thresh[df_thresh["superior_op"] == op].shape[0]
                        table += str(count)
                        if op != "equal": 
                            improvement = f"{float(df_thresh[f"{op}_improvement"].mean()):.3f}"
                            table += f" & {improvement} & "
                        else:
                            table += " \\\\ \n"
                table += "\\bottomrule\n"
                table += "\\end{tabular}\n\n"
                f.write(wrap_table(str(table), "customsize"))

if __name__ == "__main__" :

    if len(sys.argv) < 4:
        print("Usage: python3 AnalyzeNumerical.py <input_file_count> <input_file_agg> <output_folder>")
        exit(1)
    
    input_file_count, input_file_agg = sys.argv[1], sys.argv[2]
    output_folder = sys.argv[3]

    analyze_numerical(input_file_count, input_file_agg, output_folder)