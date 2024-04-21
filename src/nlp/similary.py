import voyageai
import pickle
import json
import numpy as np
from ..constants import VOYAGE_API_KEY, VOYAGE_EMBED_BATCH_SIZE

def load_topics_embeddings():
    embeddings = pickle.load(open('./data/topics-embeddings.pkl', 'rb'))
    return embeddings

def save_topics_embeddings():
    # I assume the cosistency of the data
    with open('./data/topics.txt', 'r') as f:
        topics = f.read().split('\n')
        embeddings = embed(topics)            
        pickle.dump(embeddings, open('./data/topics-embeddings.pkl', 'wb'))

def load_topics_correlation_matrix():
    mat_embedd = pickle.load(open('./data/topics-corr-matrix.pkl', 'rb'))
    return mat_embedd

def save_topics_correlation_matrix():
    topics_embedd = load_topics_embeddings()
    embeddings = np.array([x['embedding'] for x in topics_embedd])
    sim = len(embeddings) * [[]]
    for i, t in enumerate(embeddings):
        for j, tt in enumerate(embeddings):
            sim[i].append({
                'id': j,
                'sim': cosine_distance(t, tt)
            })
    pickle.dump(sim, open('./data/topics-corr-matrix.pkl', 'wb'))    


def embed(texts: list[str]):
    vo = voyageai.Client(api_key=VOYAGE_API_KEY)
    embeddings = []

    for i in range(0, len(texts), VOYAGE_EMBED_BATCH_SIZE):
        batch = texts[i:i+VOYAGE_EMBED_BATCH_SIZE]
        result = vo.embed(batch, model='voyage-law-2')
        
        for j in range(len(batch)):
            embeddings.append({
                'topic': texts[i + j],
                'embedding': result.embeddings[j] 
            })
    return embeddings

def cosine_distance(x, y):
    assert len(x) == len(y), "The arrays must have the same length"
    dot = np.dot(x, y)
    n1, n2 = np.linalg.norm(x), np.linalg.norm(y)
    return dot / (n1 * n2)