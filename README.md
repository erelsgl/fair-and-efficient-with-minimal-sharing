# Fair and efficient with minimal sharing

This repository contains the experiments described in the following paper:

> [Efficient Fair Division with Minimal Sharing](https://arxiv.org/abs/1908.01669), by Fedor Sandomirskiy and Erel Segal-Halevi, Operations Research, 2022.
 
The code runs best on a Linux system. It could also run on Windows, but the time-limit feature is not supported on Windows, so the code might run for a very long time.

To install the requirements, do:
 
    pip install -r requirements.txt

The experiments are done in two steps: making the results, and analyzing the results. Making the results takes a lot of time, so it is useful to store the results first in a CSV file, and then run the analysis.

## Experiment with random instances

**Step 1**: Edit the file [make_results_random.py](make_results_random.py) to control the simulation parameters, e.g., numbers of agents, numbers of resources, and path to the results file. Then run the simulation:

    python make_results_random.py

It should create a CSV file containing the results in the specified path, e.g. `results_random/99sec.csv`.
NOTE: If the file already exists, the existing experiments will be skipped. If you want to run new experiments, either delete the file or choose a different file name.

**Step 2**: Edit the file [analyze_results.py](analyze_results.py) to control the analysis parameters, e.g., the path to the generated results file. Then analyze the results:

    python analyze_results.py

It should create graphics files in the same folder, e.g. `results_random`. Enjoy!



## Experiment with Spliddit instances

**Step -1**: To use the Spliddit data, you should first ask the team of [spliddit.org](https://spliddit.org/) to send you an SQL dump.
Then, convert it to an SQLITE database as follows:

    python mysql_to_sqlite.py <filename>.sql

It should create a file called `<filename>.db`.

**Step 0**: Edit the file [spliddit.py](spliddit.py) and update the path to the db. Then verify that it works by running:

    python spliddit.py

**Step 1**: Edit the file [make_results.py](make_results.py) to control the simulation parameters, e.g.,  path to the results file. Then run the simulation:

    python make_results.py

It should create a CSV file containing the results in the specified path, e.g. `results/99sec.csv`.
NOTE: If the file already exists, the existing experiments will be skipped. If you want to run new experiments, either delete the file or choose a different file name.

**Step 2**: Edit the file [analyze_results.py](analyze_results.py) to control the analysis parameters, e.g., the path to the generated results file. Then analyze the results:

    python analyze_results.py

It should create graphics files in the same folder, e.g. `results`. Enjoy!
