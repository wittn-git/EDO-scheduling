mkdir -p ../data/aggregated
python3 ../scripts_analysis/ConcatFiles.py ../data/runs ../data/aggregated/concatenated.csv
python3 ../scripts_analysis/SummarizeRuns.py ../data/aggregated/concatenated.csv ../data/aggregated/aggregated.csv

mkdir -p ../data/tables
python3 ../scripts_analysis/GenerateTables.py ../data/aggregated/aggregated.csv ../data/tables/table.tex