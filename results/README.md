# Results

This directory contains the experimental results obtained for some networks in `data`.


## Counting-Experiment
This directory contains the summary of the experiment in section 4.4 in our paper. 

Each file, for example `count_summary_n=3_r=4.csv`, is a summary of the results of all runs of  `code/CountSupportNetworks.py` for 100 samples with 3 leaves and 4 reticulations, which can be found in `data/Counting-Experiment/n=3_r=4`.

Each line is of the format
```
Input file, |A_N|, |B_N|, |C_N|
```
where
- `Input file` is the name of the txt file (list of the edges) in [`data/Counting-Experiment`](../data/Counting-Experiment) used for the run.
- `|A_N|` is the number of all support networks of the input networks.
- `|B_N|` is the number of minimal support networks of the input networks.
- `|C_N|` is the number of minimum support networks of the input networks.

## LM-Experiment
This directory contains the results of all runs and the summaries of the experiment in section 6.3 in our paper. This directory has two subdirectories.


### summary
This directory contains the summaries of the outputs of the experiments in Section 6.3 in our paper.

Each , for example, `exact_vs_heuristic_r=5_summary.csv`, meaning that this file compares the outputs of running `code/LM-Exact.py` and `code/LM-Heuristic.py` with the 100 samples in `data/LM-Experiment/n=8_r=5` as the inputs.

Each line is of the format
```
Input file, Exact minimum level, Heuristic minimum level, Exact runtime, Heuristic runtime
```
where
- `Input file` is the name of the txt file (list of the edges) in `data/LM-Experiment` used for the run.
- `Exact minimum level` is the true minimum level of support networks in the input network calculated by `code/LevelMinimization-Exact.py`. 
- `Heuristic minimum level` is the estimated minimum level of support networks in the input network calculated by `code/LM-Heuristic.py`. 
- `Exact runtime` is the computation time of `LM-Exact` reported by the wall-clock time.
- `Heuristic runtime` is the computation time of `LM-Heuristic` reported by the wall-clock time.

### all_output
This directory contains all the outputs of running `code/LM-Exact.py` and `code/LM-Heuristic.py` for the sample networks in `data/LM-Experiment`.

Each subdirectory is named, for example, `n=8_r=5_15`, meaning that the subdirectory contains the output(s) of `code/LM-Exact.py` and `code/LM-Heuristic.py`(only from `r=1` to `r=33`) with the input `data/LM-Experiment/n=8_r=5/n=8_r=5_15.txt`.

Each file is named, for example, `n=8_r=5_15_LMheuristic_result.txt`, meaning that this file is the output of `code/LM-Heuristic.py` with the input `data/LM-Experiment/n=8_r=5/n=8_r=5_15.txt`. 
