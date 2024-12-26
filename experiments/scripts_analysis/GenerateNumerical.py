import pandas as pd
import sys
import os

def wrap_table(table, font_name):
    return f"\\begin{{center}}\n\\renewcommand{{\\tabcolsep}}{{4pt}}\n\\renewcommand{{\\arraystretch}}{{1.1}}\n" \
           f"\\begin{{{font_name}}}\n{table}\n\\end{{{font_name}}}\n\\end{{center}}\n"

def process_table_header(diversity_operators, operator_mapping, value_column=False):
    multicolumns = ["\\multicolumn{1}{c}{Value}"] if value_column else []
    multicolumns += [f"\\multicolumn{{{'1' if op == 'equal' else '2'}}}{{c}}{{{operator_mapping[op]}}}" for op in diversity_operators]
    header = " & ".join(multicolumns) + " \\\\ \n"
    sub_headers = ["\\#Sup", "$\\uparrow$", "\\#Sup", "$\\uparrow$", "\\#"]
    if value_column:
        header += "\\cmidrule(lr){1-1} \\cmidrule(lr){2-3} \\cmidrule(lr){4-5}  \\cmidrule(lr){6-6}\n"
        sub_headers.insert(0, "Value")
    else:
        header += "\\cmidrule(lr){1-2} \\cmidrule(lr){3-4} \\cmidrule(lr){5-5}\n"
    header += " & ".join(sub_headers) + " \\\\ \n"
    return header

def process_table_rows(df_thresh, diversity_operators):
    row = ""
    for op in diversity_operators:
        count = df_thresh[df_thresh["superior_op"] == op].shape[0]
        row += f"{count}"
        if op != "equal":
            improvement = f"{float(df_thresh[f'{op}_improvement'].mean()):.5f}"
            row += f" & {improvement} "
        row += " & " if op != "equal" else ""
    return row + " \\\\ \n"

def process_value_rows(df_thresh, diversity_operators, column_combination, value_mapping):
    value_rows = ""
    values = df_thresh[column_combination].drop_duplicates().values
    for value_row in values:
        df_value = df_thresh
        for col, val in zip(column_combination, value_row):
            df_value = df_value[df_value[col] == val]
        val_str = str(value_row).replace("[", "").replace("]", "").replace("'", "")
        val_str = value_mapping.get(val_str, val_str)
        value_row_str = f"{val_str} & "
        for op in diversity_operators:
            count = df_value[df_value["superior_op"] == op].shape[0]
            value_row_str += f"{count}"
            if op != "equal":
                improvement = f"{float(df_value[f'{op}_improvement'].mean()):.3f}"
                value_row_str += f" & {improvement} & "
            else:
                value_row_str += " \\\\ \n"
        value_rows += value_row_str
    return value_rows


def analyze_numerical(input_file_count, input_file_agg, output_folder):
    df_count = pd.read_csv(input_file_count)
    df_agg = pd.read_csv(input_file_agg)

    operator_mapping = {"eucl": "$\\lVert \\cdot \\rVert_2$", "sum": "$\\Sigma \\cdot$", "equal": "Equal"}
    column_combination_mapping = {"mu": "Population Size", "n": "Number of Jobs", "m": "Number of Machines", "alpha": "Quality Parameter", "mutation_operator": "Mutation Operator"}
    value_mapping = {"XRAI_0.10": "X(R+I), $\\lambda=0.1$", "XRAI_1.00": "X(R+I), $\\lambda=1$", "XRAI_1.50": "X(R+I), $\\lambda=1.5$", "1RAI": "1(R+I)"}

    diversity_operators = list(df_agg["diversity_operator"].unique()) + ["equal"]
    diversity_thresholds = df_count["diversity_threshold"].unique()

    column_combinations = [["mu"], ["n"], ["m"], ["alpha"], ["mutation_operator"]]

    font_name = "customnormal"

    for diversity_threshold in diversity_thresholds:
        df_thresh = df_count[df_count["diversity_threshold"] == diversity_threshold]
        output_file = os.path.join(output_folder, f"table_numerical_div[{diversity_threshold:.2f}].tex")

        with open(output_file, "w") as f:
            table = "\\begin{tabular}{rrrrr}\n"
            table += "\\multicolumn{5}{l}{Overall}\\\\\n"
            table += "\\toprule\n"
            table += process_table_header(diversity_operators, operator_mapping)
            table += "\\midrule\n"
            table += process_table_rows(df_thresh, diversity_operators)
            table += "\\bottomrule\n"
            table += "\\end{tabular}\n\n"
            f.write(wrap_table(str(table), font_name))
            f.write("\n\n")

            for column_combination in column_combinations:
                title = column_combination_mapping.get("_".join(column_combination), "_".join(column_combination))
                table = "\\begin{tabular}{lrrrrr}\n"
                table += f"\\multicolumn{{6}}{{l}}{{{title}}}\\\\\n"
                table += "\\toprule\n"
                table += process_table_header(diversity_operators, operator_mapping, value_column=True)
                table += "\\midrule\n"
                table += process_value_rows(df_thresh, diversity_operators, column_combination, value_mapping)
                table += "\\bottomrule\n"
                table += "\\end{tabular}\n\n"
                f.write(wrap_table(str(table), font_name))

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python3 AnalyzeNumerical.py <input_file_count> <input_file_agg> <output_folder>")
        exit(1)

    input_file_count, input_file_agg = sys.argv[1], sys.argv[2]
    output_folder = sys.argv[3]

    analyze_numerical(input_file_count, input_file_agg, output_folder)
