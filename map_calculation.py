from ehi_utils              import load_json, dict2dotdict, dotdict2dict
from gem.evaluation         import evaluate_graph_reconstruction as gr
from load_graph_embedding   import load_embedding
import numpy as np
import pickle

# evaluate embedding
def evaluate_embedding(graph, embedding):   
    class _Dummy(object):
        def __init__(self, embedding):
            self.embedding = embedding

        def get_reconstructed_adj(self, X=None, node_l=None):
            node_num = self.embedding.shape[0]
            adj_mtx_r = np.zeros((node_num, node_num))
            for v_i in range(node_num):
                for v_j in range(node_num):
                    if v_i == v_j:
                        continue
                    adj_mtx_r[v_i, v_j] = self.get_edge_weight(v_i, v_j)
            return adj_mtx_r
        
        def get_edge_weight(self, i, j):
            return np.dot(self.embedding[i, :], self.embedding[j, :])

    dummy_model = _Dummy(embedding)
    MAP, prec_curv, err, err_baseline = gr.evaluateStaticGraphReconstruction(graph, dummy_model, embedding, None)
    return (MAP, prec_curv)

# Change the name of the dataset
dataset = "pastebin"
json_path = f"./data/{dataset}/config.json"
configs = load_json(json_path)
configs = dict2dotdict(configs)

timespells = configs.timespells
graph_embeddings = {}
reconstruction_performance = {}
reconstruction_performance_curve = {}
for ts in range(1, int(timespells)+1):
    f = open(f"{configs.DATA_PATH}/TS{str(ts)}/generated/graphs.pkl", 'rb')
    graph, graph_str = pickle.load(f)
    f.close()    
    for model in configs.models:
        if model not in graph_embeddings.keys():
            graph_embeddings[model] = {}
            reconstruction_performance[model] = {}
            reconstruction_performance_curve[model] = {}
        graph_embeddings[model][ts] = load_embedding(f"{configs.EMBEDDING_PATH}/TS{ts}/{model}.nv")
        reconstruction_performance[model][ts], reconstruction_performance_curve[model][ts] = evaluate_embedding(graph.G, graph_embeddings[model][ts])

f = open(f"{configs.RESULT_PATH}/MAP.csv", "w")
header = "Model, " + ", ".join(["TS" + str(i) for i in range(1, timespells + 1)]) + "\n"
for model in configs.models:
    row = model + ", " + ", ".join([str(reconstruction_performance[model][i]) for i in range(1, timespells + 1)]) + "\n"
    f.write(row)
f.close()