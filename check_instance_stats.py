""" 
A utility program for checking a single instance from the SPLIDDIT database.

Author: Erel Segal-Halevi
Since:  2020-2021
"""

from fairpy.valuations import ValuationMatrix
from fairpy.allocations import Allocation, AllocationMatrix

from fairpy.items.min_sharing_impl.FairEnvyFreeAllocationProblem import FairEnvyFreeAllocationProblem
from fairpy.items.min_sharing_impl.FairProportionalAllocationProblem import FairProportionalAllocationProblem
from fairpy.items.min_sharing_impl.FairMaxProductAllocationProblem import FairMaxProductAllocationProblem
from fairpy.items.min_sharing_impl.FairAllocationProblem import ErrorAllocationMatrix

from spliddit import spliddit_instance, spliddit_instances_ids

import numpy as np

if __name__ == "__main__":
    resource_counts = []
    agent_counts = []
    for id in spliddit_instances_ids():
        instance = spliddit_instance(id)
        agent_counts.append(instance.shape[0])
        resource_counts.append(instance.shape[1])
    resource_counts = np.array(resource_counts)
    print(f"mean: {resource_counts.mean()}. median: {np.median(resource_counts)}. max: {resource_counts.max()}. min: {resource_counts.min()}.")
    print(resource_counts)

    agent_counts = np.array(agent_counts)
    print(f"mean: {agent_counts.mean()}. median: {np.median(agent_counts)}. max: {agent_counts.max()}. min: {agent_counts.min()}.")
    print(agent_counts)