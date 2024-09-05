#pragma once

#include <functional>
#include <vector>

#include "../utility/generating.hpp"

using T = std::vector<std::vector<int>>;
using L = int;

// Evaluation Operators -------------------------------------------------------------

/*
    Tardyjobs Evaluation: Evaluates machine schedules based on the number of tardy jobs
    Arguments:
        - processing_times: Times it takes to complete each job
        - due_dates:        Points in time where every job is due
*/

std::function<std::vector<L>(const std::vector<T>&)> evaluate_tardyjobs(MachineSchedulingProblem problem) { 
    int n = problem.processing_times.size();
    return [problem, n](const std::vector<T>& genes) -> std::vector<L> {
        std::vector<L> fitnesses(genes.size());
        std::transform(genes.begin(), genes.end(), fitnesses.begin(), [&](const T& gene) -> double {
            int tardy_jobs_n = 0;
            for(auto schedule : gene){
                int current_time = 0;
                for(auto it = schedule.begin(); it != schedule.end(); it++){
                    current_time += problem.processing_times[*it];
                    if(current_time > problem.due_dates[*it]){
                        tardy_jobs_n++;
                    }
                }
            }
            return (double) tardy_jobs_n;
        });
        return fitnesses;
    };
}