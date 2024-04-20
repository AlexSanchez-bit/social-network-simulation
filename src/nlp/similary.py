import voyageai
import pickle
import json
import numpy as np
from ..constants import VOYAGE_API_KEY, VOYAGE_EMBED_BATCH_SIZE

def load_topics_embeddings():
    embeddings = pickle.load(open('./data/topic-embed.pkl', 'rb'))
    return embeddings

def save_topics_embeddings():
    vo = voyageai.Client(api_key=VOYAGE_API_KEY)

    # I assume the cosistency of the data
    with open('./data/topics.txt', 'r') as f:
        topics = f.read().split('\n')
        embeddings = embed(topics)            
        pickle.dump(embeddings, open('./data/topic-embed.pkl', 'wb'))    
        with open('./data/topic-embed.json', 'w') as f:
            f.write(json.dumps(embeddings))

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