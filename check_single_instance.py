""" 
A utility program for checking a single instance from the SPLIDDIT database.

Author: Erel Segal-Halevi
Since:  2020-2021
"""

from fairpy.items.valuations import ValuationMatrix
from fairpy.allocations import Allocation, AllocationMatrix

from fairpy.items.min_sharing_impl.FairEnvyFreeAllocationProblem import FairEnvyFreeAllocationProblem
from fairpy.items.min_sharing_impl.FairProportionalAllocationProblem import FairProportionalAllocationProblem
from fairpy.items.min_sharing_impl.FairMaxProductAllocationProblem import FairMaxProductAllocationProblem

from spliddit import spliddit_instance

import numpy as np


import logging, sys
logger = logging.getLogger(__name__)

logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel(logging.INFO)


def product_of_utilities(allocation:AllocationMatrix, valuation:ValuationMatrix):
    allocation = Allocation(valuation, allocation)
    return np.exp(sum(np.log(allocation.utility_profile())))


def debug_instance(instance_id, time_limit_in_seconds=1000):
    valuation_matrix = ValuationMatrix(spliddit_instance(instance_id))
    print("\nInstance: ", instance_id, "\nValuations: \n", valuation_matrix, flush=True)
    print("{} agents, {} resources".format(valuation_matrix.num_of_agents, valuation_matrix.num_of_objects), flush=True)

    problem = FairProportionalAllocationProblem(valuation_matrix)
    (prop_status, prop_time_in_seconds, prop_allocation) = \
        problem.find_min_sharing_allocation_with_time_limit(time_limit_in_seconds=time_limit_in_seconds)
    print("\nProportional Allocation: \n", prop_allocation, flush=True)
    prop_product = product_of_utilities(prop_allocation, valuation_matrix)
    print("Status: {}, #sharing: {}, product: {}, time: {}".format(prop_status, prop_allocation.num_of_sharings(), prop_product, prop_time_in_seconds), flush=True)

    problem = FairEnvyFreeAllocationProblem(valuation_matrix)
    (ef_status, ef_time_in_seconds, ef_allocation) = \
            problem.find_min_sharing_allocation_with_time_limit(time_limit_in_seconds=time_limit_in_seconds)
    print("\nEnvy-Free Allocation: \n", ef_allocation, flush=True)
    ef_product = product_of_utilities(ef_allocation, valuation_matrix)
    print("Status: {}, #sharing: {}, product: {}, time: {}".format(ef_status, ef_allocation.num_of_sharings(), ef_product, ef_time_in_seconds), flush=True)

    # (maxprod_status, maxprod_time_in_seconds, maxprod_num_sharing, maxprod_allocation, maxprod_product) = \
    #     find_max_product_allocation_and_sharing(valuation_matrix, time_limit_in_seconds=time_limit_in_seconds)

    problem = FairMaxProductAllocationProblem(valuation_matrix)
    (maxprod_status, maxprod_time_in_seconds, maxprod_allocation) = \
            problem.find_min_sharing_allocation_with_time_limit(time_limit_in_seconds=time_limit_in_seconds)
    print("\nMax-product Allocation: \n", maxprod_allocation, flush=True)
    maxprod_product = product_of_utilities(maxprod_allocation, valuation_matrix)
    print("Status: {}, #sharing: {}, product: {}, time: {}".format(maxprod_status, maxprod_allocation.num_of_sharings(), maxprod_product, maxprod_time_in_seconds), flush=True)


if __name__ == "__main__":
    debug_instance(65533)  # many sharings in max-product allocation
