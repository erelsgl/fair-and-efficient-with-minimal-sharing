""" 
A main program for analyzing the experiment results.
The result file should be generated first by `make_results.py`.

Author: Erel Segal-Halevi
Since:  2020-2021
"""

import pandas
from check_single_instance import debug_instance
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

import logging, sys
logger = logging.getLogger(__name__)
from multibar import multibar

logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel(logging.INFO)


def print_results_by_numagents_and_status(results_csv_file:str, status_column_name:str, output_file:str):
    """
    Find the number and percentage of instances that completed correctly (without timeout or error)
    """
    results = pandas.read_csv(results_csv_file)
    results = results.query("prop_status!='Duplicate'")
    results_by_num_agents_and_prop_status = results.groupby(["num_agents",status_column_name]).agg({"instance_id":"count"}).rename(columns={"instance_id":"count"})
    results_by_num_agents  = results.groupby(["num_agents"]).agg({"instance_id":"count"}).rename(columns={"instance_id":"count"})
    results_by_num_agents_and_prop_status["percent"] = np.round(results_by_num_agents_and_prop_status.div(results_by_num_agents, level="num_agents")*100)
    results = results_by_num_agents_and_prop_status.reset_index()

    csv_output = ""

    # Add a row per num-agents:
    for num_agents in sorted(results.num_agents.unique()):
        results_numagents = results.loc[results.num_agents==num_agents]
        try:
            total_count = results_numagents["count"].sum()
            total_percent = results_numagents["percent"].sum()
            ok_count = results_numagents.loc[results[status_column_name]=="OK"]["count"].sum()
            ok_percent = results_numagents.loc[results[status_column_name]=="OK"]["percent"].sum()
        except IndexError:
            ok_count = ok_percent = 0
        csv_output += "{},{},{},{},{}".format(num_agents,total_count,total_percent,ok_count,ok_percent) + "\n"

    # Add the total row:
    total_count = results["count"].sum()
    total_percent = 100.0
    ok_count = results.loc[results[status_column_name] == "OK"]["count"].sum()
    ok_percent = np.round(ok_count*100/ total_count,1)
    csv_output += "{},{},{},{},{}".format("Total", total_count, total_percent, ok_count, ok_percent) + "\n"

    csv_output = "num_agents,total_count,total_percent,ok_count,ok_percent\n" + csv_output
    print(csv_output)
    with open(output_file, 'w') as f: f.write(csv_output)


def print_results_by_numresources_and_status(results_csv_file:str, status_column_name:str, output_file:str):
    """
    Find the number and percentage of instances that completed correctly (without timeout or error)
    """
    results = pandas.read_csv(results_csv_file)
    results = results.query("prop_status!='Duplicate'")
    results_by_num_resources_and_prop_status = results.groupby(["num_resources",status_column_name]).agg({"instance_id":"count"}).rename(columns={"instance_id":"count"})
    results_by_num_resources  = results.groupby(["num_resources"]).agg({"instance_id":"count"}).rename(columns={"instance_id":"count"})
    results_by_num_resources_and_prop_status["percent"] = np.round(results_by_num_resources_and_prop_status.div(results_by_num_resources, level="num_resources")*100)
    results = results_by_num_resources_and_prop_status.reset_index()

    csv_output = ""

    # Add a row per num-resources:
    for num_resources in sorted(results.num_resources.unique()):
        results_numresources = results.loc[results.num_resources==num_resources]
        try:
            total_count = results_numresources["count"].sum()
            total_percent = results_numresources["percent"].sum()
            ok_count = results_numresources.loc[results[status_column_name]=="OK"]["count"].sum()
            ok_percent = results_numresources.loc[results[status_column_name]=="OK"]["percent"].sum()
        except IndexError:
            ok_count = ok_percent = 0
        csv_output += "{},{},{},{},{}".format(num_resources,total_count,total_percent,ok_count,ok_percent) + "\n"

    # Add the total row:
    total_count = results["count"].sum()
    total_percent = 100.0
    ok_count = results.loc[results[status_column_name] == "OK"]["count"].sum()
    ok_percent = np.round(ok_count*100/ total_count,1)
    csv_output += "{},{},{},{},{}".format("Total", total_count, total_percent, ok_count, ok_percent) + "\n"

    csv_output = "num_resources,total_count,total_percent,ok_count,ok_percent\n" + csv_output
    print(csv_output)
    with open(output_file, 'w') as f: f.write(csv_output)


def print_results_by_numagentsresources_and_status(results_csv_file:str, status_column_name:str, output_file:str):
    """
    Find the number and percentage of instances that completed correctly (without timeout or error)
    """
    results = pandas.read_csv(results_csv_file)
    results = results.query("prop_status!='Duplicate'")
    results_by_nums_and_prop_status = results.groupby(["num_agents","num_resources",status_column_name]).agg({"instance_id":"count"}).rename(columns={"instance_id":"count"})
    results = results_by_nums_and_prop_status.reset_index()

    csv_output = ""

    # Add a row per num-resources:
    for num_agents in sorted(results.num_agents.unique()):
        for num_resources in sorted(results.num_resources.unique()):
            results_nums = results.loc[(results.num_resources==num_resources) & (results.num_agents==num_agents)]
            try:
                total_count = results_nums["count"].sum()
                ok_count = results_nums.loc[results[status_column_name]=="OK"]["count"].sum()
            except IndexError:
                ok_count = 0
            if total_count > 0:
                csv_output += "{},{},{},{}".format(num_agents,num_resources,total_count,ok_count) + "\n"

    # Add the total row:
    total_count = results["count"].sum()
    ok_count = results.loc[results[status_column_name] == "OK"]["count"].sum()
    csv_output += "{},{},{},{}".format("Total", "Total", total_count, ok_count) + "\n"

    csv_output = "num_agents,num_resources,total_count,ok_count\n" + csv_output
    print(csv_output)
    with open(output_file, 'w') as f: f.write(csv_output)





def print_buggy_instances(results_csv_file:str):
    """
    Find instances in which the number of sharings is more than n-1.
    """
    results = pandas.read_csv(results_csv_file)
    ef_bugs = results.loc[results.ef_status=="Bug"]
    if len(ef_bugs)>0:
        print("EF bugs:", ef_bugs)
    for instance_id in ef_bugs["instance_id"]:
        debug_instance(instance_id)

figsize=(5, 7)
dpi=80
facecolor='w'
edgecolor='k'


def plot_results_by_agents_and_resources(results_csv_file:str, figure_title:str, status_column_name:str, sharings_column_name:str, output_file:str):
    results = pandas.read_csv(results_csv_file)
    results = results.loc[results[status_column_name]=="OK"]
    nums_agents = [2,3,4,5]
    nums_resources = [3,4,5]

    fig = plt.figure(figsize=figsize, dpi=dpi, facecolor=facecolor, edgecolor=edgecolor)
    fig.suptitle(figure_title)
    axis = None
    for num_agents in nums_agents:
        results_numagents = results.loc[results.num_agents==num_agents]
        results_numagents_numresources = results_numagents.groupby("num_resources").agg({"instance_id":"count"})
        print(results_numagents_numresources)
        axis = plt.subplot(len(nums_agents),1,num_agents-nums_agents[0]+1)
        axis.set_title("{} agents".format(num_agents))
        previous_counts = np.zeros(len(nums_resources))
        for num_sharing in range(num_agents):
            map_num_resources_to_instance_count = np.zeros(len(nums_resources))
            sub_results = results_numagents.query(sharings_column_name+"=="+str(num_sharing)+" and num_resources<={}".format(max(nums_resources)))
            for num_resources, row in sub_results.groupby(["num_resources"]).count().iterrows():
                if num_resources>=nums_resources[0]:
                    count_for_numresources_numsharing = row["instance_id"]
                    total_for_numresources = results_numagents_numresources.loc[num_resources, "instance_id"].sum()
                    percent_for_numresources_numsharing = 100*count_for_numresources_numsharing/total_for_numresources
                    map_num_resources_to_instance_count[num_resources-nums_resources[0]] = percent_for_numresources_numsharing
            print("num_agents={}, num_sharing={}, counts={}".format(num_agents,num_sharing,map_num_resources_to_instance_count))
            color = (max(0,1-num_sharing*0.25), max(0,1-num_sharing*0.25), max(0,1-num_sharing*0.25))
            axis.bar(nums_resources, map_num_resources_to_instance_count, color=color, edgecolor="black", bottom=previous_counts)
            axis.set_xticks([])
            axis.set_ylabel("%instances")
            previous_counts += map_num_resources_to_instance_count
    axis.set_xlabel("#resources")
    axis.set_xticks(nums_resources)
    plt.savefig(output_file)


def num_sharing_to_grayscale(num_sharing:int)->float:
    """
    Convert a number to a grayscale color, for display
    """
    # intensity = max(0,1-num_sharing*0.25)
    intensity = 0.7**num_sharing
    return (intensity,intensity,intensity)

def plot_results_by_agents(results_csv_file:str, figure_title:str, column_name:str, output_file:str):
    status_column_name =   column_name+"_status"
    time_column_name =     column_name+"_time_in_seconds"
    sharings_column_name = column_name+"_num_sharing"

    max_num_resources = 999

    results = pandas.read_csv(results_csv_file)
    results = results.loc[(results[status_column_name]=="OK") | (results[status_column_name]=="TimeOut")]
    results = results.loc[results.num_resources <= max_num_resources]

    nums_agents = [[2], [3], [4], [5,6], [7,8]]

    map_numagents_to_heights = {}
    _, axis = plt.subplots(1,1)
    axis.set_title(figure_title, fontsize=15)
    xticks = []
    xtick_labels = []
    for index,num_agents in enumerate(nums_agents):
        max_num_sharings = max(num_agents)
        max_num_sharing_in_data = 0
        colors = [num_sharing_to_grayscale(num_sharing) for num_sharing in range(max_num_sharings+1)]
        heights = np.zeros(max_num_sharings+1)
        results_with_numagents = results.loc[results.num_agents.isin(num_agents)]
        ok_results_with_numagents = results_with_numagents.loc[results_with_numagents[status_column_name]=="OK"]
        num_instances_with_numagents =  len(results_with_numagents)
        if num_instances_with_numagents==0:
            print(f"No instances with {num_agents} agents.")
            continue
        num_ok_instances_with_numagents = len(ok_results_with_numagents)
        for num_sharing in range(max_num_sharings+1):
            num_instances_with_numsharing = sum(results_with_numagents[sharings_column_name]==num_sharing)
            if num_instances_with_numsharing>0:
                max_num_sharing_in_data=num_sharing
            heights[num_sharing] = 100 * num_instances_with_numsharing / num_instances_with_numagents
        map_numagents_to_heights[index] = heights
        xticks.append(index)
        xtick_labels.append(f"{num_agents} agents:\n{num_ok_instances_with_numagents}/{num_instances_with_numagents} completed.\n <= {max_num_sharing_in_data} sharings")
    multibar(axis, map_numagents_to_heights, colors)
    axis.set_ylabel("%instances",fontsize=15)
    axis.set_xticks(xticks)
    axis.set_xticklabels(xtick_labels)
    axis.tick_params(axis='x', which='major', labelsize=12)
    axis.tick_params(axis='y', which='major', labelsize=15)

    fig = plt.gcf()
    fig.set_size_inches(len(nums_agents)*2+3, 7)
    plt.savefig(output_file+".pdf", format="pdf")


STYLES=["r*-","go-","b.-","y.-","k.-","c.-"]

def plot_time_by_resources(results_csv_file:str, figure_title:str, column_name:str, output_file:str):
    status_column_name =   column_name+"_status"
    time_column_name =     column_name+"_time_in_seconds"
    sharings_column_name = column_name+"_num_sharing"

    nums_agents = [2,3,4,5,6,7]
    max_num_resources = 999
    max_num_sharings = 999

    results = pandas.read_csv(results_csv_file)
    results = results.loc[(results[status_column_name]=="OK") | (results[status_column_name]=="TimeOut")]
    # results = results.loc[results[time_column_name]>=0]
    results = results.loc[results["num_resources"] <= max_num_resources]
    results = results.loc[results[sharings_column_name] <= max_num_sharings]
    results = results.loc[results[sharings_column_name] >= 0]

    _, axis = plt.subplots(1,1)
    axis.set_title(figure_title)

    # group_by_column_name = "num_resources"
    group_by_column_name = sharings_column_name

    def plot(num_agents, times):
        times.plot(legend=True, style=STYLES[num_agents-2])
        axis.set_xlabel("# sharings",fontsize=15)
        # axis.set_xlabel("# objects",fontsize=15)
        axis.set_ylabel("seconds",fontsize=15)
        axis.tick_params(axis='both', which='major', labelsize=12)
        axis.xaxis.set_major_locator(MaxNLocator(integer=True))


    axis.clear()
    for num_agents in nums_agents:
        results_numagents = results.loc[results.num_agents==num_agents]
        plot(num_agents,
            results_numagents.groupby([group_by_column_name])[time_column_name].max().rename(f"{num_agents} agents"))
        plt.savefig(output_file+"_maxtime.png")

    axis.clear()
    for num_agents in nums_agents:
        results_numagents = results.loc[results.num_agents==num_agents]
        plot(num_agents,
            results_numagents.groupby([group_by_column_name])[time_column_name].median().rename(f"{num_agents} agents"))
        plt.savefig(output_file+"_medtime.png")

    axis.clear()
    for num_agents in nums_agents:
        results_numagents = results.loc[results.num_agents==num_agents]
        plot(num_agents,
            results_numagents.groupby([group_by_column_name])[time_column_name].count().rename(f"{num_agents} agents"))
        plt.savefig(output_file+"_count.png")



def compare_sharings_by_agents(results_csv_file:str, column_name:str):
    status_column_name =   column_name+"_status"
    sharings_column_name = column_name+"_num_sharing"

    max_num_agents = 8
    max_num_resources = 999

    results = pandas.read_csv(results_csv_file)
    results = results.loc[(results[status_column_name]=="OK") | (results[status_column_name]=="TimeOut")]
    results = results.loc[results.num_agents <= max_num_agents]
    results = results.loc[results.num_resources <= max_num_resources]

    total = results.count()[sharings_column_name]
    better_than_worstcase = results.query(f"{sharings_column_name} < num_agents-1").count()[sharings_column_name]
    better_than_ceei = results.query(f"{sharings_column_name} < maxprod1_num_sharing").count()[sharings_column_name]
    print(f"{sharings_column_name}: better_than_worstcase={better_than_worstcase}/{total}={better_than_worstcase/total*100}%, better_than_ceei={better_than_ceei}/{total}={better_than_ceei/total*100}%")
    print(sharings_column_name, ": ", results.query(f"{sharings_column_name} < num_agents").count()[sharings_column_name])



def plot_time_by_agents(results_csv_file:str, figure_title:str, column_name:str, output_file:str):
    status_column_name =   column_name+"_status"
    time_column_name =     column_name+"_time_in_seconds"

    max_num_resources = 999
    max_num_agents = 8

    results = pandas.read_csv(results_csv_file)

    results = results.loc[(results[status_column_name]=="OK") | (results[status_column_name]=="TimeOut")]
    results = results.loc[results["num_resources"] <= max_num_resources]
    results = results.loc[results["num_agents"] <= max_num_agents]

    # for column_name in ["prop", "ef", "maxprod1"]:
    #     time_column_name =     column_name+"_time_in_seconds"
    #     results[time_column_name] = results[time_column_name].apply(np.log)

    _, axis = plt.subplots(1,1)
    axis.set_title(figure_title)
    axis.clear()
    results.groupby(["num_agents"])["prop_time_in_seconds"].median().rename(f"fPO+PROP").plot(legend=True, style="b-+", logy=True)
    results.groupby(["num_agents"])["ef_time_in_seconds"].median().rename(f"fPO+EF").plot(legend=True, style="g-o", logy=True)
    results.groupby(["num_agents"])["maxprod1_time_in_seconds"].median().rename(f"0.999-CEEI").plot(legend=True, style="r-", logy=True)
    axis.set_xlabel("# agents",fontsize=12)
    axis.set_ylabel("Median run-time [seconds]",fontsize=12)
    plt.savefig(output_file+".pdf", format="pdf")


def analysis_for_operations_research_paper(folder, results_file):
    plot_time_by_agents(results_file, "Log median time to find a min-sharing PROP allocation", "prop", folder + "/runtime")
    plot_results_by_agents(results_file, "Minimum #sharings in a PROP allocation", "prop", folder + "/sharing_prop")
    plot_results_by_agents(results_file, "Minimum #sharings in an EF allocation", "ef", folder + "/sharing_ef")
    plot_results_by_agents(results_file, "Minimum #sharings in a 0.999-CEEI allocation", "maxprod1", folder + "/sharing_ceei")


def analysis_for_random_instances():
    folder = "7-results-random"
    results_file = folder+"/99sec.csv"
    
    print_buggy_instances(results_file)

    print_results_by_numagents_and_status(results_file,"prop_status", folder+"/timeout_agents_prop.csv")
    print_results_by_numagents_and_status(results_file,"ef_status", folder+"/timeout_agents_ef.csv")

    print_results_by_numresources_and_status(results_file,"prop_status", folder+"/timeout_resources_prop.csv")
    print_results_by_numresources_and_status(results_file,"ef_status", folder+"/timeout_resources_ef.csv")

    print_results_by_numagentsresources_and_status(results_file,"prop_status", folder+"/timeout_nums_prop.csv")
    print_results_by_numagentsresources_and_status(results_file,"ef_status", folder+"/timeout_nums_ef.csv")

    plot_time_by_resources(results_file, "Median time to find a min-sharing PROP allocation", "prop", folder + "/prop")
    plot_time_by_resources(results_file, "Median time to find a min-sharing EF allocation", "ef", folder + "/ef")
    plot_time_by_resources(results_file, "Median time to find a min-sharing 0.999-CEEI allocation", "maxprod1", folder + "/ceei")

    plot_time_by_agents(results_file, "Log median time to find a min-sharing PROP allocation", "prop", folder + "/runtime")

    plot_results_by_agents(results_file, "Minimum #sharings in a PROP allocation", "prop", folder + "/sharing_prop.png")
    plot_results_by_agents(results_file, "Minimum #sharings in an EF allocation", "ef", folder + "/sharing_ef.png")
    plot_results_by_agents(results_file, "Minimum #sharings in a 0.999-CEEI allocation", "maxprod1", folder + "/sharing_ceei.png")

    compare_sharings_by_agents(results_file,  "prop")
    compare_sharings_by_agents(results_file,  "ef")



if __name__ == "__main__":
    folder = "results_random" # "results" # 
    results_file = folder+"/99sec.csv" # folder+"/999sec.csv" # 
    analysis_for_operations_research_paper(folder, results_file)
