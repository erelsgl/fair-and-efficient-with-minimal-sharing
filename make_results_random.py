""" 
A main program for running experiments with random data.

Author: Erel Segal-Halevi
Since:  2020-2021
"""

from fairpy import ValuationMatrix
from check_single_instance import product_of_utilities

from fairpy.items.min_sharing_impl.FairEnvyFreeAllocationProblem import FairEnvyFreeAllocationProblem
from fairpy.items.min_sharing_impl.FairProportionalAllocationProblem import FairProportionalAllocationProblem
from fairpy.items.min_sharing_impl.FairMaxProductAllocationProblem import FairMaxProductAllocationProblem

import numpy as np

def solve_random_instance(instance_id:int, num_agents:int, num_resources:int, time_limit_in_seconds=998):
    valuation_matrix = np.random.rand(num_agents, num_resources)
    valuation_matrix = ValuationMatrix(valuation_matrix)
    print("\nInstance: ", instance_id, "\nValuations: \n", valuation_matrix)
    print("{} agents, {} resources".format(valuation_matrix.num_of_agents, valuation_matrix.num_of_objects), flush=True)

    problem = FairProportionalAllocationProblem(valuation_matrix)
    (prop_status, prop_time_in_seconds, prop_allocation) = \
        problem.find_min_sharing_allocation_with_time_limit(time_limit_in_seconds=time_limit_in_seconds)
    prop_product = product_of_utilities(prop_allocation,valuation_matrix)

    problem = FairEnvyFreeAllocationProblem(valuation_matrix)
    (ef_status, ef_time_in_seconds, ef_allocation) = \
        problem.find_min_sharing_allocation_with_time_limit(time_limit_in_seconds=time_limit_in_seconds)
    ef_product = product_of_utilities(ef_allocation,valuation_matrix)

    TOLERANCE = 0.001
    problem = FairMaxProductAllocationProblem(valuation_matrix, tolerance=TOLERANCE)
    (maxprod1_status, maxprod1_time_in_seconds, maxprod1_allocation) = \
        problem.find_min_sharing_allocation_with_time_limit(time_limit_in_seconds=time_limit_in_seconds)
    maxprod1_product = product_of_utilities(maxprod1_allocation,valuation_matrix)

    print("\nProportional Allocation: \n", prop_allocation)
    print("Status: {}, #sharing: {}, product: {}, time: {}".format(prop_status, prop_allocation.num_of_sharings(), prop_product, prop_time_in_seconds))
    print("\nEnvy-Free Allocation: \n", ef_allocation)
    print("Status: {}, #sharing: {}, product: {}, time: {}".format(ef_status, ef_allocation.num_of_sharings(), ef_product, ef_time_in_seconds))
    print(f"\n{TOLERANCE}-Max-product Allocation: \n", maxprod1_allocation)
    print("Status: {}, #sharing: {}, product: {}, time: {}".format(maxprod1_status, maxprod1_allocation.num_of_sharings(), maxprod1_product, maxprod1_time_in_seconds))
    print(flush=True)

    return {
        "prop_status": prop_status,
        "prop_time_in_seconds": prop_time_in_seconds,
        "prop_num_sharing": prop_allocation.num_of_sharings(),
        "prop_product": prop_product,
        "ef_status": ef_status,
        "ef_time_in_seconds": ef_time_in_seconds,
        "ef_num_sharing": ef_allocation.num_of_sharings(),
        "ef_product": ef_product,
        "maxprod1_status": maxprod1_status,
        "maxprod1_time_in_seconds": maxprod1_time_in_seconds,
        "maxprod1_num_sharing": maxprod1_allocation.num_of_sharings(),
        "maxprod1_product": maxprod1_product,
    }



if __name__ == "__main__":
    import logging, experiments
    experiments.logger.setLevel(logging.INFO)
    experiment = experiments.Experiment("results_random/", "99sec.csv", "results/backups/")
    
    input_ranges = {
        "instance_id": range(20),
        "num_agents": [2,3],
        "num_resources": [2,4,6,8],
        "time_limit_in_seconds": [99]
    }
    experiment.run(solve_random_instance, input_ranges)

    input_ranges = {
        "instance_id": range(20),
        "num_agents": [4],
        "num_resources": [2,4,6],
        "time_limit_in_seconds": [99]
    }
    experiment.run(solve_random_instance, input_ranges)
