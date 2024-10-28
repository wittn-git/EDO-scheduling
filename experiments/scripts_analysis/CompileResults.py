import sys
import os

def compile_tables(output_file, include_plots, input_folder_plots, include_numerical, input_folder_numerical, include_tables, input_folder_tables):

    with open(output_file, "w") as f:

        f.write('''\\documentclass{article}\n\\usepackage{array}\n\\usepackage{booktabs}\n\\usepackage{svg}\n\\usepackage{amsmath}\n\\usepackage{multirow}\n\\usepackage[table]{xcolor}\n\\usepackage{hhline}\n\\definecolor{lightgray}{RGB}{211, 211, 211}\n\\usepackage[margin=0cm]{geometry} \n\\usepackage{relsize} \n\\newcommand{\\customsize}{\\relsize{-3.5}} \n\\begin{document}\n''')
        
        if include_tables:
            table_files = sorted([table_file for table_file in os.listdir(input_folder_tables) if table_file.endswith(".tex")])
            for table_file in table_files:
                f.write(f"\\verb|{input_folder_tables + "/" + table_file}|\n")
                f.write(f"\\input{{{input_folder_tables + "/" + table_file}}}\n")
                f.write("\\newpage\n")
        
        if include_plots:
            plot_files = sorted([plot_file for plot_file in os.listdir(input_folder_plots) if plot_file.endswith(".svg")])
            for plot_file in plot_files:
                f.write(f"\\verb|{input_folder_plots + "/" + plot_file}|\n")
                f.write(f"\\begin{{figure}}[t]\n\\centering\n")
                f.write(f"\\includesvg[width=0.7\\textwidth]{{{input_folder_plots + "/" + plot_file}}}\n")
                f.write("\\vskip-8pt\n\\end{figure}\n")
                f.write("\\newpage\n")
        
        if include_numerical:
            #TODO implement this
            pass

        f.write("\\end{document}")
        
if __name__ == "__main__" :

    if len(sys.argv) < 8:
        print("Usage: python3 CompileResult.py <output_file> <include_folder_plots> <input_plots> <include_folder_numerical> <input_numerical> <include_folder_tables> <input_tables>")
        exit(1)
    
    output_file = sys.argv[1]
    include_plots, input_folder_plots = sys.argv[2] == "True", sys.argv[3]
    include_numerical, input_folder_numerical = sys.argv[4] == "True", sys.argv[5]
    include_tables, input_folder_tables = sys.argv[6] == "True", sys.argv[7]
    
    compile_tables(output_file, include_plots, input_folder_plots, include_numerical, input_folder_numerical, include_tables, input_folder_tables)