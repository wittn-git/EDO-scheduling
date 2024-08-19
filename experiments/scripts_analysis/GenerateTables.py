import sys
import pandas as pd

def generate_table(input_file : str, output_file : str):

    with open(input_file, "r") as f:
        df = pd.read_csv(f)
    
    font_name = "tiny"
    parameter_columns = {"mu": "$\\mu$", "n": "$n$", "m": "$m$", "alpha": "$\\alpha$"}
    groups = df.groupby(list(parameter_columns.keys()))
    def get_group_count(index, current_key):
        count = 0
        for key, group in groups:
            key_valid = True
            for i in range(index + 1):
                if current_key[i] != key[i]: 
                    key_valid = False
                    break
            if key_valid: count += 1
        return count
    
    parameter_indices = {parameter: 0 for i, parameter in enumerate(parameter_columns.keys())}
    inner_columns = {
        "diversity": "$Div$",
        "generations": "$Gen$",
        "max_generations": "$Gen_{max}$"
    }
    operators = df["mutation"].unique()
    operator_display_names = {
        "1RAI": "1(R+I)"
    }

    with open(output_file, "w") as f:
        f.write("\\begin{center}\n\\renewcommand{\\tabcolsep}{4pt}\n\\renewcommand{\\arraystretch}{1.1}\n") # basic table starting commands
        f.write(f"\\begin{{{font_name}}}\n") # setting the font size
        f.write(f"\\begin{{tabular}}{{cccc*{{{len(inner_columns) * len(operators)}}}{{>{{\\raggedleft\\arraybackslash}}p{{1cm}}}}}}\n\\toprule\n") # setting the table column format
        f.write(f"\\multicolumn{{{len(parameter_columns)}}}{{c}}{{}} & ") # spacing for the first 4 columns
        
        for i, operator in enumerate(operators):
            if operator in operator_display_names.keys(): operator = operator_display_names[operator]
            f.write(f"\\multicolumn{{{len(inner_columns)}}}{{c}}{{{operator}}}")
            if i != len(operators) - 1: f.write(" & ")
            else: f.write(" \\\\ \n")

        for i, operator in enumerate(operators): # lines under the operator names
            f.write(f"\\cmidrule(lr){{{len(parameter_columns)+1+i*len(inner_columns)}-{len(parameter_columns)+1+i*len(inner_columns)+len(inner_columns)-1}}} ")
        f.write("\n")

        for column in parameter_columns.values(): # writing the parameter names
            f.write(f"{column} & ")
        
        for i, operator in enumerate(operators): # writing the inner columns names
            for j, inner_column in enumerate(inner_columns.values()):
                f.write(f"{inner_column}")
                if i != len(operators) - 1 or j != len(inner_columns) - 1: f.write(" & ")
        f.write(" \\\\ \n")
            
        f.write("\\midrule\n") # line under the parameter names
        
        for group_index, (key, group) in enumerate(groups): # iterate the groups of the dataframe
            if group_index != 0:
                for i, column in enumerate(parameter_columns.keys()): # draw the hhline if end of the group is reached
                    if parameter_indices[column] == 0 and i != len(parameter_columns) - 1:
                        f.write(f"\\hhline{{{i*'~'}{(len(parameter_columns)+len(operators)*len(inner_columns)-i)*'-'}}}\n")
                        break
            for i, column in enumerate(parameter_columns.keys()):
                if parameter_indices[column] == 0:
                    group_count = get_group_count(i, key)
                    f.write(f"\\multirow{{{group_count}}}{{*}}{{{key[i]}}}")
                    parameter_indices[column] = group_count - 1
                    if i != len(parameter_columns) - 1: hhline = i
                else:
                    parameter_indices[column] -= 1
                f.write(" & ")
            for i, operator in enumerate(operators): # write the values of the inner columns
                operator_group = group[group["mutation"] == operator]
                for j, inner_column in enumerate(inner_columns.keys()):
                    f.write(f"{operator_group[inner_column].mean():.3f}")
                    if i != len(operators) - 1 or j != len(inner_columns) - 1: f.write(" & ")
            f.write(" \\\\ \n")      

        f.write(f"\\end{{tabular}} \n \\end{{{font_name}}} \n \\end{{center}}") # basic table ending commands

if __name__ == "__main__" :

    if len(sys.argv) < 3:
        print("Usage: python3 GenerateTables.py <input_file> <output_file>")
        exit(1)
  
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    generate_table(input_file, output_file)