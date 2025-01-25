import sys
import os

def get_substring_between(s, start, end):
    start_index = s.find(start)+1
    end_index = s[start_index:].find(end) + start_index
    return s[start_index:end_index]

def get_preamble(data_packages_file):
    s = "\\documentclass{article} \n \\usepackage[margin=2cm]{geometry} \n \\usepackage[inkscapearea=page,inkscapeversion=1.2.2]{svg} \n"
    s += f"\\input{{{data_packages_file}}}"
    return s + '''
                \\newcommand{\\runningtitle}{Evolutionary Diversity Optimization for Parallel Machine Scheduling}
                \\newcommand{\\runningauthors}{D. Wittner and Jakob Bossek}

                \\begin{document}

                \\title{\\textbf{Evolutionary Diversity Optimization} \\\\ \\textbf{for Parallel Machine Scheduling} \\\\ \\vspace{0.8em} \\Large Experimental Results}

                \\author{Dominic Wittner\\inst{1}\\orcidID{0009-0008-1290-9541} and Jakob Bossek\\inst{2}\\orcidID{0000-0002-4121-4668}}
                \\institute{
                \\inst{1}RWTH Aachen, Aachen, Germany\\\\
                \\email{dominic.wittner@rwth-aachen.de}
                \\and
                \\inst{2}Paderborn University, Paderborn, Germany\\\\
                \\email{jakob.bossek@uni-paderborn.de}
                }

                \\date{}

                \\maketitle
                \\begin{center}
                \\begin{tabular}{c}
                \\inst{1}RWTH Aachen, Aachen, Germany\\\\
                \\email{dominic.wittner@rwth-aachen.de}\\\\
                \\inst{2}Paderborn University, Paderborn, Germany\\\\
                \\email{jakob.bossek@uni-paderborn.de}
                \\end{tabular}
                \\end{center}

                \\begin{small}
                \\noindent The following document contains a full account of the experimental results obtained from the experiments conducted for the paper \\enquote{Evolutionary Diversity Optimization for Parallel Machine Scheduling} by Dominic Wittner and Jakob Bossek. 
                It contains the following sections:

                \\begin{itemize}
                    \\item \\textbf{Section 1:} The plots of the part of the experiments, that can also be found in the paper.
                    \\item \\textbf{Section 2:} An account of the data aggregated over the runs for each instance. There exists one table for each diversity threshold and mutation operator. Each cell corresponds to the average value of an attribute of 30 runs of the in the paper presented parameter configurations by the label of columns and rows. FOr each parameter set and diversity operator, the following fields are displayed:
                    \\begin{itemize}
                        \\item $Rob_I$: The percentage of robustness tests passed by the initial population.
                        \\item $Div$: The diversity of the population.
                        \\item $Gen$: The ratio of the number of passed generations and the maximum number of generations.
                        \\item $Rob_F$: The percentage of robustness tests passed by the final population.
                    \\end{itemize}
                    \\item \\textbf{Section 3:} An account of the the superiority of the diversity operators. For each diversity threshold, there is a table giving, for each operator, the count of instances, where the it lead to the passing of the robustness test while the other one did not. It also includes the average improvement of the robustness as well as the count of instances, where the operators had equal results. To rule out, that some parameter might be responsible for the superiority, the tables are also split by the parameter configurations. The following fields are displayed:
                    \\begin{itemize}
                        \\item \\#Sup: The count of instances, where the operator lead to the passing of the robustness test while the other one did not.
                        \\item $\\uparrow$: The average improvement of the robustness.
                        \\item \\#: The count of instances, where the operators had equal results.
                    \\end{itemize}
                \\end{itemize}
                \\end{small}
                \\tableofcontents
                \\newpage
        '''

def compile(output_file, include_plots, input_folder_plots, include_numerical, input_folder_numerical, include_tables, input_folder_tables, data_packages_file):

    with open(output_file, "w") as f:
        
        f.write(get_preamble(data_packages_file))

        f.write("\\newpage\n\\section{Plots}\n")
        if include_plots:
            description_map ={
                "clusterexample.svg": "Diversity calculated using the Euclidean norm in relation to cumulative similarity with a maximum pairwise similarity of 50 and population size 50.",
                "countplot.svg": "Visualization of the difference of superiority in terms of robustness between the methods of transforming the vector of similarities, i.e. the difference of the number of instances where $\\lVert \\cdot \\rVert _2$ lead to a passed robustness test and $\\Sigma \\cdot$ did not and the reverse (positive values indicating more frequent superiority of $\\lVert \\cdot \\rVert_2$, negative values analogue for $\\Sigma \\cdot$), for each parameter group.",
                "generationplot.svg": "Average of the ratio of the generations passed until termination and the maximum number of generations for different parameter groups.",
                "percentageplot.svg": "Improvement of robustness from initial robustness to robustness at the respective diversity threshold over all instances of both methods to summarize the vector of similarities.",
                "percentageplot_sixfold.svg": "Improvement of robustness from initial robustness to robustness at the respective diversity threshold over all instances of using $\\lVert \\cdot \\rVert_2$ to summarize the vector of similarities, for each parameter group."
            }
            plot_files = sorted([plot_file for plot_file in os.listdir(input_folder_plots) if plot_file.endswith(".svg")])
            for plot_file in plot_files:
                f.write(f"\\begin{{figure}}[H]\n\\centering\n")
                f.write(f"\\includesvg[width=0.7\\textwidth]{{{input_folder_plots + "/" + plot_file}}} \\caption{{{description_map[plot_file]}}}\n")
                f.write("\\vskip-8pt\n\\end{figure}\n")

        f.write("\\newpage\n\\section{Numerical Results}\n") 
        if include_numerical:
            table_files = sorted([table_file for table_file in os.listdir(input_folder_numerical) if table_file.endswith(".tex")])
            for table_file in table_files:
                threshold = get_substring_between(table_file, "[", "]")
                f.write(f"\\verb|Diversity Threshold: {threshold}|\n")
                f.write(f"\\input{{{input_folder_numerical + "/" + table_file}}}\n")
                f.write("\\newpage\n")
        
        f.write("\\newpage\n\\section{Tables}\n")
        if include_tables:
            mutation_mapping = {"XRAI_0.10": "X(R+I), $\\lambda=0.1$", "XRAI_1.00": "X(R+I), $\\lambda=1$", "XRAI_1.50": "X(R+I), $\\lambda=1.5$", "1RAI": "1(R+I)"}
            table_files = sorted([table_file for table_file in os.listdir(input_folder_tables) if table_file.endswith(".tex")])
            for table_file in table_files:
                threshold = get_substring_between(table_file, "[", "]")
                mutation_operator = get_substring_between(table_file, "-", "-")
                f.write(f"\\verb|Diversity Threshold: {threshold}, Mutation Operator: |")
                f.write(mutation_mapping[mutation_operator] + "\n")
                f.write(f"\\input{{{input_folder_tables + "/" + table_file}}}\n")
                f.write("\\newpage\n")

        f.write("\\end{document}")
        
if __name__ == "__main__" :

    if len(sys.argv) < 9:
        print("Usage: python3 CompileResult.py <output_file> <include_folder_plots> <input_plots> <include_folder_numerical> <input_numerical> <include_folder_tables> <input_tables> <data_packages_file>")
        exit(1)
    
    output_file = sys.argv[1]
    include_plots, input_folder_plots = sys.argv[2] == "True", sys.argv[3]
    include_numerical, input_folder_numerical = sys.argv[4] == "True", sys.argv[5]
    include_tables, input_folder_tables = sys.argv[6] == "True", sys.argv[7]
    data_packages_file = sys.argv[8]
    
    compile(output_file, include_plots, input_folder_plots, include_numerical, input_folder_numerical, include_tables, input_folder_tables, data_packages_file)