"""
A utility function to create a multi-bar-chart in matplotlib.

AUTHOR: Erel Segal-Halevi
SINCE:  2020-07-06
"""

import matplotlib.pyplot as plt
import numpy as np
from typing import Dict, List


def multibar(axis, map_xvalues_to_yvalues:Dict[float,List], colors:List[tuple], edgecolor="black"):
    """
    Plots a bar-plot in which each bar is made of several accumulating bars of different colors.

    :param axis: the pyplot Axis object for the plot.
    :param map_xvalues_to_yvalues: maps each x-value to a list of y-values representing heights.
    :param colors: a list of RGB tuples representing colors. colors[0] is the color of the lowest bars, then colors[1], etc.
    """
    # color = (max(0, 1 - num_sharing * 0.25), max(0, 1 - num_sharing * 0.25), max(0, 1 - num_sharing * 0.25))
    # axis.bar(nums_resources, map_num_resources_to_instance_count, color=color, edgecolor="black",
    #          bottom=previous_counts)
    # print(map_xvalues_to_yvalues)
    xvalues = map_xvalues_to_yvalues.keys()
    bottom_heights = np.zeros(len(xvalues))
    for y_index,color in enumerate(colors):
        current_heights = np.zeros(len(xvalues))
        for x_index,yvalues in enumerate(map_xvalues_to_yvalues.values()):
            if y_index<len(yvalues):
                current_heights[x_index] = yvalues[y_index]
            else:
                current_heights[x_index] = 0
        axis.bar(xvalues, current_heights, color=color, edgecolor=edgecolor, bottom=bottom_heights)
        bottom_heights += current_heights

if __name__=="__main__":
    multibar(plt,
             {2: [1,2,3], 3: [2,3,1], 4:[3,1,4]},
             colors=[(0,0,.5),(0,.3,.7),(0,.5,1)],
            )
    # should show 3 bars of height 6, 6, 7. In each bar there should be 3 shades of blue.
    plt.show()


