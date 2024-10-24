mkdir -p ../data/aggregated
rm -f ../data/aggregated/concatenated.csv
rm -f ../data/aggregated/aggregated.csv
python3 ../scripts_analysis/ConcatFiles.py ../data/runs ../data/aggregated/concatenated.csv
python3 ../scripts_analysis/SummarizeRuns.py ../data/aggregated/concatenated.csv ../data/aggregated/aggregated.csv

mkdir -p ../data/tables
rm -f ../data/tables/*
div_thresholds=("0" "0.1" "0.25" "0.4" "0.5" "0.65" "0.75" "0.8" "0.85" "0.9" "0.95" "1")

for div_threshold in "${div_thresholds[@]}"; do
    python3 ../scripts_analysis/GenerateTables.py ../data/aggregated/aggregated.csv ../data/tables $div_threshold
done
python3 ../scripts_analysis/CompileTables.py ../data/tables
pdflatex -output-directory=../data/tables ../data/tables/compiled_tables.tex

mus=("2" "5" "10" "25")
ns=("5" "10" "15" "25" "50")
ms=("1" "3" "5")
alphas=("0.3" "0.6" "1")
operators=("1RAI" "XRAI_0.10" "XRAI_1.50" "XRAI_1.00")

for operator in "${operators[@]}"; do
    for mu in "${mus[@]}"; do
        for n in "${ns[@]}"; do
            for m in "${ms[@]}"; do
                for alpha in "${alphas[@]}"; do
                    python3 ../scripts_analysis/PlotTrajectoryGraph.py ../data/aggregated/aggregated.csv ../data/plots $mu $n $m $alpha $operator
                done
            done
        done
    done
done
