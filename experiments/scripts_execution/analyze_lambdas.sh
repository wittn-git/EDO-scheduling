echo "Analyzing lambdas without euclidean norm"
python3 ../scripts_analysis/AnalyzeLambdas.py ../data/other/preliminary_lambda_res.csv 0
echo "Analyzing lambdas with euclidean norm"
python3 ../scripts_analysis/AnalyzeLambdas.py ../data/other/preliminary_lambda_res.csv 1