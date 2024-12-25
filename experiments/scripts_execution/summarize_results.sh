if [ "$#" -ne 9 ]; then
    # to run a full summary, set all arguments (9) to True
    echo "Usage: bash summarize_results.sh <aggregate> <count_data> <create_plots> <create_numerical> <create_tables> <compile_results> <compile_plots> <compile_numerical> <compile_tables>"
    exit 1
fi

if [ "$1" = "True" ]; then
    mkdir -p ../data/aggregated
    rm -f ../data/aggregated/concatenated.csv
    rm -f ../data/aggregated/aggregated.csv
    rm -f ../data/aggregated/counted.csv
    python3 ../scripts_analysis/ConcatFiles.py ../data/runs ../data/aggregated/concatenated.csv
    python3 ../scripts_analysis/AggregateRuns.py ../data/aggregated/concatenated.csv ../data/aggregated/aggregated.csv ../data/aggregated/counted.csv
fi

if [ "$2" = "True" ]; then
    python3 ../scripts_analysis/CountData.py ../data/aggregated/concatenated.csv
fi

if [ "$3" = "True" ]; then
    mkdir -p ../data/plots
    rm -f ../data/plots/*
    python3 ../scripts_analysis/PlotCounts.py ../data/aggregated/counted.csv ../data/plots svg
    mus=("2" "5" "10" "25")
    ns=("5" "10" "15" "25" "50")
    for mu in "${mus[@]}"; do
        for n in "${ns[@]}"; do
            python3 ../scripts_analysis/PlotTrajectoryGraph.py ../data/aggregated/aggregated.csv ../data/plots svg $mu $n
        done
    done
fi

if [ "$4" = "True" ]; then 
    mkdir -p ../data/numerical
    rm -f ../data/numerical/*
    python3 ../scripts_analysis/AnalyzeNumerical.py ../data/aggregated/counted.csv ../data/aggregated/aggregated.csv ../data/numerical
fi

if [ "$5" = "True" ]; then
    mkdir -p ../data/tables
    rm -f ../data/tables/*
    div_thresholds=()
    for i in $(seq 0 0.05 1); do
        div_thresholds+=($i)
    done
    for div_threshold in "${div_thresholds[@]}"; do
        python3 ../scripts_analysis/GenerateTables.py ../data/aggregated/aggregated.csv ../data/tables $div_threshold
    done
fi

if [ "$6" = "True" ]; then
    python3 ../scripts_analysis/CompileResults.py ../data/other/result_file.tex $7 ../data/plots $8 ../data/numerical $9 ../data/tables
    pdflatex -output-directory=../data/other -shell-escape ../data/other/result_file.tex
    rm -f ../data/other/result_file.aux ../data/other/result_file.log 
    rm -r svg-inkscape
fi
