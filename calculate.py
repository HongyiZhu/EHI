import os
import warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
warnings.filterwarnings('ignore')
import tensorflow as tf
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

from load_graph_embedding   import load_embedding
from build_embedding        import *
from graph_embedding_config import *
from ehi_utils              import load_json, dict2dotdict, dotdict2dict
from embedding_comparison   import *
from pathlib                import Path
import argparse

def main(configs):
    timespells = configs.timespells
    Path(configs.RESULT_PATH).mkdir(parents=True, exist_ok=True)
    
    # calculate for each model
    for model in configs.models:
        # load embeddings across time spells
        embs = []
        dist_ts = []
        cos_ts = []
        for ts in range(1, int(timespells)+1):
            embs.append(load_embedding(f"{configs.EMBEDDING_PATH}/TS{ts}/{model}.nv"))
        for i in range(1, int(timespells)):
            e_prev = embs[i-1]
            e_new = embs[i]
            e_new_rotated = get_rotated_embedding(e_prev, e_new, [j for j in range(e_prev.shape[0])])
            dist = get_embedding_distance(e_prev, e_new_rotated)
            cos = get_embedding_cosine(e_prev, e_new_rotated)
            dist_ts.append(dist)
            cos_ts.append(cos)

        # export to csv
        f = open(f"{configs.RESULT_PATH}/{model}.csv", "w")
        header = "NodeID, " + ", ".join(["Shift" + str(i) for i in range(1, timespells)]) + \
            ", " + ", ".join(["Sim" + str(i) for i in range(1, timespells)]) + "\n"
        f.write(header)
        n_nodes = max([len(l) for l in dist_ts])
        for i in range(n_nodes):
            dists = []
            coss = []
            for j in range(len(dist_ts)):
                if i < len(dist_ts[j]):
                    dists.append(str(dist_ts[j][i]))
                    coss.append(str(cos_ts[j][i]))
                else:
                    dists.append(" ")
                    coss.append(" ")
            row = "{}, ".format(str(i)) + ", ".join(dists) + ", " + ", ".join(coss) + "\n"
            f.write(row)
        f.close()


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