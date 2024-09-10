mkdir -p ../data/aggregated
rm -f ../data/aggregated/concatenated.csv
rm -f ../data/aggregated/aggregated.csv
python3 ../scripts_analysis/ConcatFiles.py ../data/runs ../data/aggregated/concatenated.csv
python3 ../scripts_analysis/SummarizeRuns.py ../data/aggregated/concatenated.csv ../data/aggregated/aggregated.csv

mkdir -p ../data/tables
rm -f ../data/tables/*
div_thresholds=("0.25" "0.50" "0.75" "0.85" "1.00")

for div_threshold in "${div_thresholds[@]}"; do
    python3 ../scripts_analysis/GenerateTables.py ../data/aggregated/aggregated.csv ../data/tables $div_threshold
done
python3 ../scripts_analysis/CompileTables.py ../data/tables
pdflatex -output-directory=../data/tables ../data/tables/compiled_tables.tex