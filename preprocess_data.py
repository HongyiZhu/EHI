from ehi_utils          import load_json, dict2dotdict
import argparse

def main(configs):
    timespells = configs.timespells
    for ts in range(1, int(timespells)+1):
        features = f"{configs.DATA_PATH}/TS{str(ts)}/features.csv"
        print(f"\nProcessing feature file of TS{str(ts)}")
        output_features = f"{configs.DATA_PATH}/TS{str(ts)}/generated/user.features"

        nodes = {}
        # read nodes
        f = open(configs.node_file, 'r')
        for i, l in enumerate(f.readlines()):
            # repoID => nodeID mapping
            nodes[l.strip()] = str(i)
        f.close()

        # read lines
        f = open(features, 'r')
        g = open(output_features, 'w')
        # skip csv header
        if configs.feature_header:
            f.readline()
        for l in f.readlines():
            # convert userID to nodeID
            try:
                vec = l.strip().split(",")
                g.write("{} ".format(nodes[vec[0]]))
                g.write(" ".join(vec[1:]))
                g.write("\n")
            except:
                vec = l.strip().split(",")
                print(f"node {vec[0]} not in the graph")
        g.close()
        f.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parser feature file generator")
    parser.add_argument("--json_path", type=str, required=True,help="Path to the json config file")
    args = parser.parse_args()

    configs = load_json(args.json_path)
    main(dict2dotdict(configs))
