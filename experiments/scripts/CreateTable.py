import pandas as pd

def read_csv_to_latex(csv_file, shown_header, actual_header, grouping_attribute, decimal_columns, include_entries=[], footnotesize=True):
    df = pd.read_csv(csv_file)

    if(include_entries):
        df = df.loc[include_entries]

    for column in actual_header:
        if(column in decimal_columns):
            df[column] = df[column].apply(lambda x: f"{x:.2f}")
        else:
            df[column] = df[column].apply(lambda x: f"{x:.0f}")
    
    latex_table = "\\begin{center}\n"
    latex_table += "\\renewcommand{\\tabcolsep}{4pt}\n"
    latex_table += " \\renewcommand{\\arraystretch}{1.1}\n"
    if footnotesize: latex_table += " \\begin{footnotesize}\n"
    latex_table += f" \\begin{{{'tabular'}}}{{{'r'*len(shown_header)}}}\n"
    latex_table += " \\toprule\n"
    latex_table += " & ".join(shown_header) + "\\\\ \n"

    included_attributes = []
    occurence_dict = {}
    for attribute in grouping_attribute:
        included_attributes.append(attribute)
        grouped = df.groupby(included_attributes)
        for row in grouped.size().reset_index().values:
            keys = [str(x) for x in row[:-1]]
            occurence_dict[",".join(keys)] = row[-1]
    
    currents = {attr: -1 for attr in grouping_attribute}
    for i, row in df.iterrows():
        columns = []
        new_group = False
        for attribute in actual_header:
            if(attribute not in currents):
                columns.append(row[attribute])
                continue
            if(currents[attribute] == -1 or currents[attribute] != row[attribute] or new_group):
                if(not new_group): 
                    new_group = True
                    latex_table += f"\cline{{{grouping_attribute.index(attribute)+1}-{len(actual_header)}}}\n"
                currents[attribute] = row[attribute]
                occ_keys = []
                for attr in grouping_attribute:
                    occ_keys.append(str(int(currents[attr])))
                    if(attr == attribute): break
                columns.append(f"\multirow{{{occurence_dict[','.join(occ_keys)]}}}{{{'*'}}}{{{row[attribute]}}}")
            else: columns.append("")
        latex_table += " & ".join(columns) + "\\\\ \n"

    latex_table += " \\bottomrule\n"
    latex_table += "  \end{tabular}\n"
    if footnotesize: latex_table += " \end{footnotesize}\n"
    latex_table += " \end{center}\n"
    return latex_table

if __name__ == "__main__":
    
    #csv_file = "res_constrained.csv"
    csv_file = "res_constrained.csv"
    #header = ["$\mu$", "$n$", "$m$", "$D_0$", "\\textbf{mean}", "\\textbf{std}"]
    header = ["$\mu$", "$n$", "$m$", "$\\alpha$", "$D_0$", "\\textbf{mean}", "\\textbf{std}"]
    #columns = ['mu', 'n', 'm', 'diversity', 'generations', 'std_generations']
    columns = ['mu', 'n', 'm', 'alpha', 'diversity', 'generations', 'std_generations']
    #grouping = ['mu', 'n']
    grouping = ['mu', 'n', 'm']
    #res_file = "table_constrained.tex"
    res_file = "table_constrained.tex"
    #decimal_columns = ['diversity', 'generations', 'std_generations']
    decimal_columns = ['diversity', 'generations', 'std_generations', 'alpha']
    #include_entries = [0,1,6,13,16,17,18,21,31,32,33,34,35,44,49,50]
    include_entries = [0,2,7,10,11, 55, 64,76,77,100,109,124,160,161,165,167]
    print("Number of entries:", len(include_entries))
    
    latex_table = read_csv_to_latex(csv_file, header, columns, grouping, decimal_columns, include_entries, False)
    with open(res_file, 'w') as f:
        f.write(latex_table)