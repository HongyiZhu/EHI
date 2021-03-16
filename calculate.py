from load_graph_embedding   import load_embedding
from build_embedding        import *
from graph_embedding_config import *
from ehi_utils              import load_json, dict2dotdict, dotdict2dict
import argparse

def main(configs):
    timespells = configs.timespells

    # load embeddings
    for model in configs.models:
        for ts in range(int(timespells)):
            pass

    # calculate temporal shift
    for model in configs.models:
        embs = []
        for ts in range(int(timespells)):
            embs.append(graph_embedding_ts[ts][model])

    

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