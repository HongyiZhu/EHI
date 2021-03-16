# Emerging Hacker Identification (EHI)

## Introduction

This is the code repository for the Emerging Hacker Identification project. This readme file will walk through the following components:

+ [Dependency Requirement](#dependency-requirement)
+ [Dataset](#dataset)
+ [Configurations](#configurations)
+ [Automation Logic](#automation-logic)
+ [Usage](#usage)

## Dependency Requirement

+ TensorFlow (<=1.14.0)
+ PyTorch
+ NetworkX (>=2.0)
+ GenSim
+ openpyxl
+ [OpenNE: An Open-Source Package for Network Embedding](https://github.com/thunlp/OpenNE)
+ [GEM: Graph Embedding Methods](https://github.com/palash1992/GEM)

## Dataset

### Requirement

Please format and place the following file in the corresponding folder: [node file](#node-file), [edge list](#edge-list), [feature matrix](#nodal-features).

### Node File

*Location and Name*: Place the node file under the `./data/<dataset>/` folder with the name of `'nodes.csv'`.

*Format*: Each line of the file is a userID. NodeID (used to track the network embedding) will be assigned to each userID in the given order.

```text
Example:
Filename: './data/<dataset>/nodes.csv'
3985485 (NodeID = 0)
8279795 (NodeID = 1)
8296581 (NodeID = 2)
...     (NodeID = ...)
```

### Edge List

*Location and Name*: Place the edge list of time spell `i` under the `./data/<dataset>/TS<i>` folder with the name of `'user.edgelist'`.

*Format*: An un-directional edge between nodes `a` and `b` can be denoted with `a<space>b` or `b<space>a`. Each edge takes a new line. If the graph is weighted, each edge can be denoted as `a<space>b<space>w`.

```text
Example 1 (un-weighted, default):
Filename: './data/<dataset>/TS1/user.edgelist'
0 1
1 2
3 1
. .
```

```text
Example 2 (weighted):
Filename: './data/<dataset>/TS1/user.edgelist'
0 1 1.0
1 2 0.5
3 1 0.785
. . .
```

### Nodal Features

*Location and Name*: Nodal features of time spell `i` is stored under the `./data/<dataset>/TS<i>/` folder titled `'feature.csv'`.

*Format*: For `d`-dimension nodal features, each row has `d+1` values, with userID followed by `d` features.

```csv
Example:
Filename: './data/<dataset>/features.csv'
user, f1, f2, f3, ...
3985485, 0.25, 0.35, 0.41, ...
8279795, 0.18, 0.36, 0.24, ...
...
...
```

## Configurations

All experiment configurations on graph embedding (GE) models and clustering algorithms are specified in `./graph_embedding_config.py`.

+ Change the configuration file before executing a new experiment.
+ Backup embeddings and results from the previous experiment.

## Automation Logic

The `./ehi.py` script (usage [here](#usage)) automates the following steps:

1. [Preprocessing feature files](#step-1-preprocessing)
2. [Building node embeddings](#step-2-building-node-embedding)
3. [Calculating Temporal Shifts](#step-3-calculating-temporal-shifts)

### Step 1. Preprocessing

The `./preprocess_data.py` script parse nodal feature CSVs and generate corresponding `.features` files under the `./data/<dataset>/TS<i>/` folder.

Then the `./preprocess_graph.py` script parse edge lists into graphs.

### Step 2. Building Node Embedding

The `./build.py` script builds node embeddings for the selected datset and evaluate the quality of generated embeddings.

### Step 3. Calculating Temporal Shifts

The `./calculate.py` script calculates the temporal shifts between time spells:

+ Dataset configuration: `./data/<dataset>/config.json`
+ Embeddings: `./embeddings/<dataset>/TS<i>/<GE model>.nv`  

    ```text
    #nodes #dim
    n0 e01 e02 e03 ... e0n
    n1 e11 e12 e13 ... e1n
    n2 ...
    .  ...
    ```

## Usage

```text
usage: ehi.py [-h] --dataset {pastebin} --timespells TIMESPELLS
              [--have_features HAVE_FEATURES]
              [--feature_header FEATURE_HEADER]
              [--weighted_graph WEIGHTED_GRAPH] [--models MODELS]
              [--step {P,B,C,A}]

Automated GVA Processor.

optional arguments:
  -h, --help            show this help message and exit
  --dataset {pastebin}  Process 'user' or 'repo' dataset.
  --timespells TIMESPELLS
                        The number of time spells for analysis
  --have_features HAVE_FEATURES
                        Whether the network has nodal features, default=True.
  --feature_header FEATURE_HEADER
                        Whether the feature file has a header row,
                        default=True
  --weighted_graph WEIGHTED_GRAPH
                        Whether the edges are weighted, default=False.
  --models MODELS       Comma delimited model names (e.g., TADW,GCAE,GATE),
                        default=TADW,GCAE,GATE
  --step {P,B,C,A}      Perform a particular step ([P]reprocess, [B]uild
                        embedding, [C]alculate temporal shift) or [A]ll
                        steps), default=A.
```

### *Example 1*
