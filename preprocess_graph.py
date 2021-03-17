from ehi_utils              import load_json, dict2dotdict
from mygraph                import Graph_Int, Graph_Str
import argparse
import copy
import pickle

def main(configs):
    timespells = configs.timespells
    
    # load topology
    graphs = []
    graphs_str = []
    for ts in range(1, int(timespells)+1):
        edgelist_filename = f"{configs.DATA_PATH}/TS{ts}/user.edgelist"
        graph = Graph_Int()
        graph.read_edgelist(filename=edgelist_filename, weighted=configs.weighted_graph, directed=False)
        
        graph_str = Graph_Str()
        graph_str.read_edgelist(filename=edgelist_filename, weighted=configs.weighted_graph, directed=False)
        
        graphs.append(graph)
        graphs_str.append(graph_str)
    
    # build accumulate graph
    accu_graphs = []
    accu_graphs_str = []
    for i in range(0, int(timespells)):
        if i == 0:
            accu_graphs.append(copy.deepcopy(graphs[i]))
            accu_graphs_str.append(copy.deepcopy(graphs_str[i]))
        else:
            past_graph = copy.deepcopy(accu_graphs[i-1])
            past_graph_str = copy.deepcopy(accu_graphs_str[i-1])

            # decay past edge weight
            for (src, dst) in past_graph.G.edges:
                past_graph.G[int(src)][int(dst)]['weight'] /= 2.0
                past_graph_str.G[str(src)][str(dst)]['weight'] /= 2.0

            for (src, dst) in graphs[i].G.edges:
                if past_graph.G.has_edge(int(src), int(dst)):
                    past_graph.G[int(src)][int(dst)]['weight'] += 1.0
                    past_graph_str.G[str(src)][str(dst)]['weight'] += 1.0
                else:
                    past_graph.G.add_edge(int(src), int(dst))
                    past_graph_str.G.add_edge(str(src), str(dst))
                    past_graph.G[int(src)][int(dst)]['weight'] = 1.0
                    past_graph_str.G[str(src)][str(dst)]['weight'] = 1.0
                
            accu_graphs.append(past_graph)
            accu_graphs_str.append(past_graph_str)
    for i in range(int(timespells)):
        accu_graphs[i].encode_node()
        accu_graphs_str[i].encode_node()

    # load features
    for ts in range(1, int(timespells)+1):
        if configs.have_features:
            feature_filename = f"{configs.DATA_PATH}/TS{ts}/generated/user.features"
            accu_graphs[ts-1].read_node_features(feature_filename)
            accu_graphs_str[ts-1].read_node_features(feature_filename)
        else:
            for node in accu_graphs[ts-1].G.nodes:
                accu_graphs[ts-1].G.nodes[node]['feature'] = [1,]
            for node in accu_graphs_str[ts-1].G.nodes:
                accu_graphs_str[ts-1].G.nodes[node]['feature'] = [1,]

    # save generated graphs
    for ts in range(1, int(timespells)+1):
        output_file = f"{configs.DATA_PATH}/TS{str(ts)}/generated/graphs.pkl"
        f = open(output_file, 'wb')
        pickle.dump([accu_graphs[ts-1], accu_graphs_str[ts-1]], f)
        f.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parser feature file generator")
    parser.add_argument("--json_path", type=str, required=True,help="Path to the json config file")
    args = parser.parse_args()

    configs = load_json(args.json_path)
    main(dict2dotdict(configs))