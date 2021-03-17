from ehi_utils      import dotdict2dict, dict2dotdict
from pathlib        import Path
import ast
import argparse
import subprocess
import json
import os


def get_parser():
    parser = argparse.ArgumentParser(description='Automated EHI Processor.')
    parser.add_argument("--dataset", type=str, required=True, help="Name the dataset.")
    parser.add_argument("--timespells", type=int, required=True, help="The number of time spells for analysis")

    parser.add_argument("--have_features", type=ast.literal_eval, required=False, help="Whether the network has nodal features, default=True.", default=True)
    parser.add_argument("--feature_header", type=ast.literal_eval, required=False, help="Whether the feature file has a header row, default=True", default=True)
    parser.add_argument("--weighted_graph", type=ast.literal_eval, required=False, help="Whether the edges are weighted, default=False.", default=False)

    parser.add_argument("--models", type=str, required=False, help="Comma delimited model names (e.g., TADW,GCAE,GATE), default=TADW,GCAE,GATE", default="TADW,GCAE,GATE")
    
    parser.add_argument("--step", type=str, required=False, help="Perform a particular step ([P]reprocess, [B]uild embedding, [C]alculate temporal shift) or [A]ll steps), default=A.", choices=["P", "B", "C", "A"], default="A")

    return parser

if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()
    # read arguments
    dataset = args.dataset

    # Embedding models
    # models = [
        # 'LE', 
        # 'GF', 
        # 'LLE', 
        # 'HOPE', 
        # 'GraRep',    
        # 'DeepWalk', 
        # 'node2vec',                 
        # 'SDNE',                         
        # 'LINE',                                  
        # 'GCAE',
        # 'TADW',
        # 'VGAE',
        # 'DANE',
        # 'CANE',
        # 'GATE',
    # ]
    # models = [model.upper() for model in models]

    # compile environment config file   
    configs = dict2dotdict(None)
    configs.dataset = dataset
    configs.timespells = args.timespells
    
    configs.have_features = args.have_features
    configs.feature_header = args.feature_header
    configs.weighted_graph = args.weighted_graph

    configs.models = [x.upper() for x in args.models.split(',') if x != ""]

    # paths
    configs.node_file = f"./data/{dataset}/nodes.csv"
    # configs.edgelist_filename = f"./data/{org}/{dataset}.edgelist"
    # configs.node_index_filename = f"./data/{org}/{dataset}.index"
    # configs.embedding_mapping = f"./data/{org}/{dataset}_mapping.csv"

    configs.DATA_PATH = f"./data/{dataset}/"
    configs.EMBEDDING_PATH = f"./embeddings/{dataset}/"
    
    json_configs = dotdict2dict(configs)

    json_path = f"./data/{dataset}/config.json"
    with open(json_path, 'w') as fp:
        json.dump(json_configs, fp)

    if args.step == "P" or args.step == "A":
        # create embedding folders for each time spell
        for ts in range(1, int(args.timespells)+1):
            Path(f"./data/{dataset}/TS{str(ts)}/generated").mkdir(parents=True, exist_ok=True)
            Path(f"./embeddings/{dataset}/TS{str(ts)}").mkdir(parents=True, exist_ok=True)
        if configs.have_features:
            # Run preprocess_data.py to preprocess data features
            _preprocess = subprocess.run(["python", "preprocess_data.py", "--json_path", f"{json_path}"])
        # Run preprocess_graph.py to preprocess graphs for each time spell
        _preprocess = subprocess.run(["python", "preprocess_graph.py", "--json_path", f"{json_path}"])

    if args.step == "B" or args.step == "A":
        # For each feature matrix, generate node embeddings and cluster them
        _build = subprocess.run(["python", "build.py", "--json_path", f"{json_path}"])
    # if args.step == "C" or args.step == "A":
    #     # Compare embeddings of each 
    #     _calc = subprocess.run(["python", "calculate.py", "--json_path", f"{json_path}"])

    