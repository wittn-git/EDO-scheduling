cd ../../
mkdir -p build
cd build
cmake ..
make
omp_set_num_threads=$num_cores ./EDO_scheduling $1 $2 $3 $4 $5 $6 $7 $8 $9