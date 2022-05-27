""" 
A main program for running experiments with spliddit data.

Author: Erel Segal-Halevi
Since:  2020-2021
"""

from fairpy import ValuationMatrix
from check_single_instance import product_of_utilities

from fairpy.items.min_sharing_impl.FairAllocationProblem import FairAllocationProblem, ErrorAllocationMatrix
from fairpy.items.min_sharing_impl.FairEnvyFreeAllocationProblem import FairEnvyFreeAllocationProblem
from fairpy.items.min_sharing_impl.FairProportionalAllocationProblem import FairProportionalAllocationProblem
from fairpy.items.min_sharing_impl.FairMaxProductAllocationProblem import FairMaxProductAllocationProblem

from spliddit import spliddit_instance, spliddit_instances_ids

def solve_single_instance(instance_id, time_limit_in_seconds=998):
    valuation_matrix = spliddit_instance(instance_id)
    valuation_matrix = ValuationMatrix(valuation_matrix)
    print("\nInstance: ", instance_id, "\nValuations: \n", valuation_matrix)
    print("{} agents, {} resources".format(valuation_matrix.num_of_agents, valuation_matrix.num_of_objects), flush=True)

    # prev_valuation_matrix is a static variable: https://stackoverflow.com/a/279597/827927
    if hasattr(solve_single_instance,"prev_valuation_matrix") and valuation_matrix.equals(solve_single_instance.prev_valuation_matrix):
        prop_time_in_seconds = ef_time_in_seconds = maxprod1_time_in_seconds = -1
        prop_status = ef_status = maxprod1_status = "Duplicate"
        prop_allocation = ef_allocation = maxprod1_allocation = ErrorAllocationMatrix()
    else:
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

    solve_single_instance.prev_valuation_matrix = valuation_matrix

    return {
        "num_agents": valuation_matrix.num_of_agents,
        "num_resources": valuation_matrix.num_of_objects,
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
    import logging, experiments_csv
    experiment = experiments_csv.Experiment("results/", "99sec.csv", "results/backups/")
    experiment.logger.setLevel(logging.INFO)
    input_ranges = {
        "instance_id": spliddit_instances_ids(first_id=203), 
        "time_limit_in_seconds": [99]
    }
    experiment.run(solve_single_instance, input_ranges)
