#pragma once

#include <fstream>
#include <iostream>
#include <string>
#include <sstream>

#include "../population/population.hpp"

using L = int;

void write_to_file(std::string content, std::string filename, bool append = true) {
    #pragma omp critical
    {
        std::ofstream file;
        if (append) {
            file.open(filename, std::ios_base::out | std::ios_base::app);
        } else {
            file.open(filename, std::ios_base::out | std::ios_base::trunc);
        }

        if (!file.is_open()) {
            std::cerr << "Error opening file: " << filename << std::endl;
        }else{
            file << content;
            file.close();
        }        
    }
}

template<typename... Args>
std::string get_csv_line(const Args&... args) {
    std::ostringstream oss;
    bool isFirst = true;
    ((oss << (isFirst ? "" : ",") << args, isFirst = false), ...);
    oss << "\n";
    return oss.str();
}