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

from tee_table.tee_table import TeeTable
from collections import OrderedDict

from spliddit import spliddit_instances


import numpy as np


import logging, sys
logger = logging.getLogger(__name__)

logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel(logging.INFO)

TABLE_COLUMNS = [
    "instance_id","num_agents","num_resources",
    "prop_status", "prop_time_in_seconds", "prop_num_sharing", "prop_product",
    "ef_status", "ef_time_in_seconds","ef_num_sharing", "ef_product",
    "maxprod1_status", "maxprod1_time_in_seconds","maxprod1_num_sharing", "maxprod1_product",
    "maxprod0_status", "maxprod0_time_in_seconds","maxprod0_num_sharing", "maxprod0_product",
    ]

def make_results(results_csv_file:str, first_instance_id=1, time_limit_in_seconds=998):
    """
    Read all Spliddit instances and check the minimum sharing allocation.
    """
    results_table = TeeTable(TABLE_COLUMNS, results_csv_file)

    prev_valuation_matrix = False
    for (instance_id, valuation_matrix) in spliddit_instances(first_id=first_instance_id):
        valuation_matrix = ValuationMatrix(valuation_matrix)
        print("\nInstance: ", instance_id, "\nValuations: \n", valuation_matrix)
        print("{} agents, {} resources".format(valuation_matrix.num_of_agents, valuation_matrix.num_of_objects), flush=True)

        if prev_valuation_matrix and valuation_matrix.equals(prev_valuation_matrix):
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

        results_table.add(OrderedDict((
            ("instance_id", str(instance_id)),
            ("num_agents", valuation_matrix.num_of_agents),
            ("num_resources", valuation_matrix.num_of_objects),
            ("prop_status", prop_status),
            ("prop_time_in_seconds", prop_time_in_seconds),
            ("prop_num_sharing", prop_allocation.num_of_sharings()),
            ("prop_product", prop_product),
            ("ef_status", ef_status),
            ("ef_time_in_seconds", ef_time_in_seconds),
            ("ef_num_sharing", ef_allocation.num_of_sharings()),
            ("ef_product", ef_product),
            ("maxprod1_status", maxprod1_status),
            ("maxprod1_time_in_seconds", maxprod1_time_in_seconds),
            ("maxprod1_num_sharing", maxprod1_allocation.num_of_sharings()),
            ("maxprod1_product", maxprod1_product),
        )))
        prev_valuation_matrix = valuation_matrix

    results_table.done()


if __name__ == "__main__":
    folder = "results"
    time_limit_in_seconds=999
    results_file = folder+"/999sec.csv"
    make_results(results_file, time_limit_in_seconds=time_limit_in_seconds, first_instance_id=1)
