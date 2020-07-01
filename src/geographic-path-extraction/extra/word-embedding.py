import numpy as np
from scipy import spatial
from pathlib import Path

datapath = Path(__file__).resolve().parents[2]
print(datapath)


embeddings_dict = {}

with open(datapath / "tools/glove.6B/glove.6B.300d.txt", 'r', encoding="utf-8") as f:
    for line in f:
        values = line.split()
        word = values[0]
        vector = np.asarray(values[1:], "float32")
        embeddings_dict[word] = vector

def find_closest_embeddings(embedding):
    return sorted(embeddings_dict.keys(), key=lambda word: spatial.distance.euclidean(embeddings_dict[word], embedding))

print("============================== Voyage===================================")
print(find_closest_embeddings(embeddings_dict["go"])[:10])