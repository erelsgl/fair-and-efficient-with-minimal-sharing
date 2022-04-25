""" 
A main program for analyzing experiment results that timed out.
The result file should be generated first by `make_results.py`.

Author: Erel Segal-Halevi
Since:  2020-2021
"""


from spliddit import spliddit_instance

import pandas
import numpy as np

import logging, sys
logger = logging.getLogger(__name__)

logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel(logging.INFO)

def read_timeout_results(results_csv_file:str, timeout:float):
    results = pandas.read_csv(results_csv_file)
    timeout_instances = results.query("prop_time_in_seconds > "+str(timeout))["instance_id"].to_list()

    np.set_printoptions(edgeitems=999, linewidth=100000)
    for instance_id in timeout_instances:
        valuation_matrix = spliddit_instance(instance_id)
        (num_agents, num_resources) = valuation_matrix.shape
        if num_agents <= 999:
            print("\nInstance: ", instance_id, "\nValuations: \n", valuation_matrix)
            print("{} agents, {} resources".format(num_agents,num_resources))


if __name__ == "__main__":
    results_file="5-results-2020-data/8sec.csv"
    read_timeout_results(results_file, timeout=8)
