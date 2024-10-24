import sys
import os

def compile_tables(input_folder):

    table_files = []
    for file in os.listdir(input_folder):
        if file.endswith(".tex"):
            table_files.append(file)
    
    table_files.sort()

    with open(f"{input_folder}/compiled_tables.tex", "w") as f:
        f.write('''\\documentclass{article}\n\\usepackage{array}\n\\usepackage{booktabs}\n\\usepackage{amsmath}\n\\usepackage{multirow}\n\\usepackage[table]{xcolor}\n\\usepackage{hhline}\n\\definecolor{lightgray}{RGB}{211, 211, 211}\n\\usepackage[margin=0cm]{geometry} \n\\usepackage{relsize} \n\\newcommand{\customsize}{\\relsize{-3.5}} \n\\begin{document}\n''')
        for table_file in table_files:
            f.write(f"\\verb|{table_file}|\n")
            f.write(f"\\input{{{table_file}}}\n")
            f.write("\\newpage\n")

        f.write("\\end{document}")
        
if __name__ == "__main__" :

    if len(sys.argv) < 2:
        print("Usage: python3 CompileTables.py <input_folder>")
        exit(1)
  
    input_folder = sys.argv[1]

    compile_tables(input_folder)