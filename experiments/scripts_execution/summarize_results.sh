if [ "$#" -ne 7 ]; then
    # to run a full summary, set all arguments to True
    echo "Usage: bash summarize_results.sh <aggregate> <create_plots> <create_numerical> <create_tables> <compile_plots> <compile_numerical> <compile_tables>"
    exit 1
fi

if [ "$1" = "True" ]; then
    mkdir -p ../data/aggregated
    rm -f ../data/aggregated/concatenated.csv
    rm -f ../data/aggregated/aggregated.csv
    python3 ../scripts_analysis/ConcatFiles.py ../data/runs ../data/aggregated/concatenated.csv
    python3 ../scripts_analysis/SummarizeRuns.py ../data/aggregated/concatenated.csv ../data/aggregated/aggregated.csv
fi

if [ "$2" = "True" ]; then
    mkdir -p ../data/plots
    rm -f ../data/plots/*
    mus=("2" "5" "10" "25")
    ns=("5" "10" "15" "25" "50")
    for mu in "${mus[@]}"; do
        for n in "${ns[@]}"; do
            python3 ../scripts_analysis/PlotTrajectoryGraph.py ../data/aggregated/aggregated.csv ../data/plots svg $mu $n
        done
    done
fi

if [ "$3" = "True" ]; then 
    mkdir -p ../data/numerical
    python3 ../scripts_analysis/AnalyzeNumerical.py ../data/aggregated/concatenated.csv ../data/aggregated/aggregated.csv ../data/numerical
fi

if [ "$4" = "True" ]; then
    mkdir -p ../data/tables
    rm -f ../data/tables/*
    div_thresholds=("0" "0.1" "0.25" "0.4" "0.5" "0.65" "0.75" "0.8" "0.85" "0.9" "0.95" "1")
    for div_threshold in "${div_thresholds[@]}"; do
        python3 ../scripts_analysis/GenerateTables.py ../data/aggregated/aggregated.csv ../data/tables $div_threshold
    done
fi

python3 ../scripts_analysis/CompileResults.py ../data/other/result_file.tex $5 ../data/plots $6 ../data/other $7 ../data/tables
pdflatex -output-directory=../data/other -shell-escape ../data/other/result_file.tex
rm -f ../data/other/result_file.aux ../data/other/result_file.log 
rm -r svg-inkscape