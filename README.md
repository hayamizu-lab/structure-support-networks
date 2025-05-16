# Structure Support Networks
<!-- This repository contains the Python code and experimental results for the paper "Which Phylogenetic Networks are Level-$k$ Networks with Additional Arcs? Structure and Algorithms" authored by Takatora Suzuki and Momoko Hayamizu.  -->
<!-- It includes code for computing level-$k$ and tier-$k$ support networks as well as the code for generating random phylogenetic networks and supplementary experimental results. -->

This repository contains the algorithms for solving Level Minimization problem (Problem 2 in our paper), which finding the minimum level support network and calculating this level for a given phylogenetic network. As preparation for solving this problem, we have implemented three algorithms for measuring the cardinalities of the three sets of support networks (i.e., all, minimal, and minimum support networks), which should be searched exhaustively. All of these algorithms run in linear time. We conducted experiments using this algorithm to compare the cardinalities of these sets. Furthermore, we implemented an exponential-time algorithm (Algorithm 1 in our paper) to correctly solve this problem and an exponential-time heuristic (Algorithm 2 in our paper) to approximate the solution. We conducted experiments to evaluate the accuracy and runtime of these two algorithms. This repository also includes the datasets used in each experiment, as well as the code for generating these datasets.

This repository serves as the supporting material for the paper:
> Takatora Suzuki and Momoko Hayamizu. **Which Phylogenetic Networks are Level-k Networks with Additional Arcs? Structure and Algorithms**. 

## Repository Structure

The repository is organized as follows:

* `code`: Contains all the code used for the experiments in our paper

    * `CountSupportNetworks`: Implementation of our linear-time algorithms to count the numbers of all/minimal/minimum support networks of a given network (Section 4.4)
    * `LM-Exact`: Implementation of our exact algorithm (Algorithm 1) to solve the Level Minimization Problem (Problem 2), i.e., to find a support network with the minimum level and to output the level
    * `LM-Heuristic`: Implementation of our heuristic method (Algorithm 2) to find a support network with the minimum or nearly minimum level and to output the estimated level. 
    * `Generate-Networks`: Code used to randomly generate the input data for the experiments
<!-- * `Appendix`: Includes a program used to generate the input data for the experiments (see the Appendix of our paper for details) -->
* `data`: Contains the input data used for the experiments and the corresponding results
  * `Counting-Experiment`: Data sets used in the experiment in Section 4.4
  * `LM-Experiment`: Data sets used in the experiment in Section 6.3
* `results`: Full details of the results of experiments
  * `Counting-Experiment`: Results of the experiment in Section 4.4
  * `LM-Experiment`: Results of the experiment in Section 6.3

## Usage

### Environment set-up

First, clone this repository to your local machine and access the main directory using the command below:
```bash
git clone https://github.com/hayamizu-lab/structure-support-network.git
cd structure-support-network
```

### Prerequisites
To run this project, you may require the following packages:
+ networkx
+ itertools
+ time
+ sys
+ graphviz


### Tutorial
When you run the code, you will be prompted for a file name of the input. The input must be a text file representing the list of edges of a rooted binary phylogenetic network. Here, we demonstrate the code using `sample-input.txt` (this network is isomorphic to the one shown in Figure 4 of our paper).



#### CountSpanningNetworks
When you count the numbers of all/minimal/minimum spanning networks in the input networks, use:
```terminal
python code/CountSupportNetworks.py
```
and enter 'sample-input' (without the extension). Then, you will get the results as follows:
```
Input: sample-input.txt
The number |A_N| of all support networks: 702
The number |B_N| of minimal support networks: 32
The number |C_N| of minimum support networks: 8
```



#### LM-Exact
To run the program of LM-Exact, use:
```terminal
python code/LM-Exact.py
```
and enter 'sample-input' (without the extension). Then, you will get the results as follows:
```
Input: sample-input.txt
Minimum level:1
Runtime (sec):0.004078125115483999
```
Here, this `Runtime (sec)` is the wall-clock time measured by `time.perf_counter()`.
The program will also output the visualization of the support network with minimum level in PDF format (see [`sample-input-exact.pdf`](sample-input-exact.pdf)). This PDF highlights the support network in the input network with black solid lines.
#### LM-Heuristic
To run the program of of LM-Heuristic, use:
```
python code/LM-Heuristic.py
```
and enter 'sample-input' (without the extension). Then, you will get the results as follows:

```
Input: sample-input.txt
Minimum level:2
Runtime (sec):0.0012555411085486412
```
Here, this `Runtime (sec)` is the wall-clock time measured by `time.perf_counter()`.
The program will also output the visualization of support network with minimum level in PDF format (see [`sample-input-heuristic.pdf`](sample-input-heuristic.pdf)). This PDF highlights the support network in the input network with black solid lines.


#### Notes
+ By default, the reference to the input file and the destination of the output .txt file are set to the working directory. If you want to change this, add an absolute or relative path as shown below.
    - Reference to input file
    ```python
    with open('/path/to/your/output/directory/' + filename + '.csv', 'r', encoding='utf-8') as file:
    ```
    - Save output graph to
    ```python
    draw_subnetwork(network, min_lev_network, '/path/to/your/output/directory/' + filename) #without the extension
    ```


## License

This project is licensed under the [MIT License](LICENSE).

## Contact

If you have any questions or suggestions regarding this project, please feel free to contact the authors:
- Takatora Suzuki [takatora.szk@fuji.waseda.jp](mailto:takatora.szk@fuji.waseda.jp)
- Momoko Hayamizu (Corresponding author): [hayamizu@waseda.jp](mailto:hayamizu@waseda.jp)
