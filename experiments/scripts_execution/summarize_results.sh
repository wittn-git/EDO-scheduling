if [ "$#" -ne 9 ]; then
    # to run a full summary, set all arguments (9) to True
    echo "Usage: bash summarize_results.sh <aggregate> <count_data> <create_plots> <create_numerical> <create_tables> <compile_results> <compile_plots> <compile_numerical> <compile_tables>"
    exit 1
fi

if [ "$1" = "True" ]; then
    mkdir -p ../data/aggregated
    mkdir -p ../data/other
    mkdir -p ../data/stats
    rm -f ../data/other/threshold_passing.txt
    rm -f ../data/aggregated/*
    rm -f ../data/stats/*
    python3 ../scripts_analysis/ConcatFiles.py ../data/runs ../data/aggregated/concatenated.csv
    python3 ../scripts_analysis/AggregateRuns.py ../data/aggregated/concatenated.csv ../data/aggregated/aggregated.csv ../data/aggregated/counted.csv ../data/stats
fi

if [ "$2" = "True" ]; then
    python3 ../scripts_analysis/CountData.py ../data/aggregated/concatenated.csv
fi

if [ "$3" = "True" ]; then
    mkdir -p ../data/plots
    rm -f ../data/plots/*
    mkdir -p ../data/stats
    python3 ../scripts_analysis/PlotCounts.py ../data/aggregated/counted.csv ../data/plots ../data/stats svg
    python3 ../scripts_analysis/PlotPercentagesSixfold.py ../data/aggregated/counted.csv ../data/plots ../data/stats svg
    python3 ../scripts_analysis/PlotPercentages.py ../data/aggregated/counted.csv ../data/plots ../data/stats svg
    python3 ../scripts_analysis/PlotClusterExample.py ../data/plots/clusterexample.svg 50 50 2
    python3 ../scripts_analysis/PlotGenerations.py ../data/aggregated/aggregated.csv ../data/plots svg
fi

if [ "$4" = "True" ]; then 
    mkdir -p ../data/numerical
    rm -f ../data/numerical/*
    python3 ../scripts_analysis/GenerateNumerical.py ../data/aggregated/counted.csv ../data/aggregated/aggregated.csv ../data/numerical
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
    mkdir -p ../data/other
    rm -f ../data/other/result_file.tex
    rm -f ../data/other/result_file.pdf
    python3 ../scripts_analysis/CompileResults.py ../data/other/result_file.tex $7 ../data/plots $8 ../data/numerical $9 ../data/tables ../data/other/data_packages.tex
    pdflatex -output-directory=../data/other -shell-escape ../data/other/result_file.tex
    pdflatex -output-directory=../data/other -shell-escape ../data/other/result_file.tex
    rm -f ../data/other/result_file.aux ../data/other/result_file.log 
    rm -f ../data/other/result_file.aux ../data/other/result_file.toc 
    rm -r svg-inkscape
fi