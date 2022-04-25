""" 
Fix the number of sharings for experiments that timed out.
The result file should be generated first by `make_results.py`

Author: Erel Segal-Halevi
Since:  2020-2021
"""

import pandas
import numpy as np

def fix_num_sharing(results:pandas.DataFrame):
    def new_prop_num_sharing(row):
        if row["prop_status"]!="OK":
            return row["num_agents"]-1
        else:
            return row["prop_num_sharing"]
    def new_ef_num_sharing(row):
        if row["ef_status"]!="OK":
            return row["num_agents"]-1
        else:
            return row["ef_num_sharing"]
    def new_ceei_num_sharing(row):
        if row["maxprod1_status"]!="OK":
            return row["num_agents"]-1
        else:
            return row["maxprod1_num_sharing"]
    results["prop_num_sharing"] = results.apply(new_prop_num_sharing, axis=1)
    results["ef_num_sharing"] = results.apply(new_ef_num_sharing, axis=1)
    results["maxprod1_num_sharing"] = results.apply(new_ceei_num_sharing, axis=1)




if __name__ == "__main__":
    folder = "results"
    results_file = folder+"/test.csv"
    results = pandas.read_csv(results_file)
    fix_num_sharing(results)
    results.to_csv(results_file,index=False)
