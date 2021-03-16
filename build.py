import os
import warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
warnings.filterwarnings('ignore')
import tensorflow as tf
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

from build_embedding        import *
from graph_embedding_config import *
from ehi_utils              import load_json, dict2dotdict, dotdict2dict
import argparse
import pickle
import time


def main(configs):
    timespells = configs.timespells
    graph_embedding_ts = []
    # work on each time spells
    for ts in range(1, int(timespells)+1):
        current_embedding_path = f"{configs.EMBEDDING_PATH}/TS{str(ts)}/"
        # load graphs
        print("====================\nLoading preprocessed graphs")
        t1 = time.time()
        # load preprocessed graphs of current time spell
        f = open(f"{configs.DATA_PATH}/TS{str(ts)}/generated/graphs.pkl", 'rb')
        graph, graph_str = pickle.load(f)
        f.close()
        print("Data Loaded. Time elapsed: {:.3f}\n====================\n".format(time.time() - t1))

        # build graph embeddings
        graph_embeddings = {}
        # build new graph embedding
        print("====================\nBuilding Graph Embeddings\n")
        t2 = time.time()
        for model in configs.models:
            graph_embeddings[model] = build_embedding(graph, graph_str, model, current_embedding_path, configs)


def get_parser():
    parser = argparse.ArgumentParser(description="Parser for Embedding Building")
    parser.add_argument("--json_path", type=str, required=True, help="Path to the json config file")
    return parser

if __name__ == "__main__":
    parser = get_parser()
    args = parser.parse_args()

    configs = load_json(args.json_path)
    configs = dict2dotdict(configs)
    main(configs)