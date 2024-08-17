import sys
import pandas as pd

def generate_table(input_file : str, output_file : str):

    with open(input_file, "r") as f:
        df = pd.read_csv(f)
    
    font_name = "tiny"
    parameter_columns = {"mu": "$\\mu$", "n": "$n$", "m": "$m$", "alpha": "$\\alpha$"}
    # for each parameter columns, get the first value
    parameter_columns_spacing = {col: [0, 0, df[col].values[0]] for col in parameter_columns} # first entry: current index of this column, second entry: running index of the column, third entry: next value of the column
    inner_columns = {
        "diversity": "Div",
        "starting_robustness": "R1",
        "ending_robustness": "R2"
    }
    operators = df["mutation"].unique()


    with open(output_file, "w") as f:
        f.write("\\begin{center}\n\\renewcommand{\\tabcolsep}{4pt}\n\\renewcommand{\\arraystretch}{1.1}\n") # basic table starting commands
        f.write(f"\\begin{{{font_name}}}\n") # setting the font size
        f.write(f"\\begin{{tabular}}{{cccc*{{{len(inner_columns) * len(operators)}}}{{>{{\\raggedleft\\arraybackslash}}p{{1cm}}}}}}\n\\toprule\n") # setting the table column format
        f.write(f"\\multicolumn{{{len(parameter_columns)}}}{{c}}{{}} & ") # spacing for the first 4 columns
        
        for i, operator in enumerate(operators): # writing the operator names
            f.write(f"\\multicolumn{{{len(inner_columns)}}}{{c}}{{{operator}}}")
            if i != len(operators) - 1: f.write(" & ")
            else: f.write(" \\\\ \n")

        for i, operator in enumerate(operators): # lines under the operator names
            f.write(f"\\cmidrule(lr){{{len(parameter_columns)+1+i*len(inner_columns)}-{len(parameter_columns)+1+i*len(inner_columns)+len(inner_columns)-1}}} ")
        f.write("\n")

        for column in parameter_columns.keys(): # writing the parameter names
            f.write(f"{column} & ")
        
        for i, operator in enumerate(operators): # writing the inner columns names
            for j, inner_column in enumerate(inner_columns.values()):
                f.write(f"{inner_column}")
                if i != len(operators) - 1 or j != len(inner_columns) - 1: f.write(" & ")
        f.write(" \\\\ \n")
            
        f.write("\\midrule\n") # line under the parameter names

        # iterate the groups of the dataframe


        '''
            for j, column in enumerate(parameter_columns):
                if parameter_columns_spacing[column][0] == 0: # managing the multirows for the parameter columns
                    value_occurrences = df[df[column] == parameter_columns_spacing[column][1]].shape[0]
                    f.write(f"\\multirow{{{value_occurrences}}}{{*}}{{{parameter_columns_spacing[column][2]}}}")
                    parameter_columns_spacing[column][0] = value_occurrences
                    parameter_columns_spacing[column][1] += value_occurrences
                    parameter_columns_spacing[column][2] = df[column].values[parameter_columns_spacing[column][1]]
                else:
                    parameter_columns_spacing[column][0] -= 1
                f.write(" & ")

            for j, operator in enumerate(operators):
                for k, inner_column in enumerate(inner_columns):
                    # get the value of the inner columns of the current row of this operator
                   
                    if j != len(operators) - 1 or k != len(inner_columns) - 1: f.write(" & ")  
            f.write(" \\\\ \n")
        '''
        #TODO finish

        f.write(f"\\end{{tabular}} \n \\end{{{font_name}}} \n \\end{{center}}") # basic table ending commands


if __name__ == "__main__" :

    if len(sys.argv) < 3:
        print("Usage: python3 GenerateTables.py <input_file> <output_file>")
        exit(1)
  
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    generate_table(input_file, output_file)