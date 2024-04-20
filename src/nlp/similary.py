import voyageai
import pickle
import json
from ..constants import VOYAGE_API_KEY, VOYAGE_EMBED_BATCH_SIZE

def load_topics_embeddings():
    embeddings = pickle.load(open('./topic-embed.pkl', 'rb'))
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
        result = vo.embed(batch, model='voyage-lite-02-instruct')
        
        for j in range(len(batch)):
            embeddings.append({
                'topic': texts[i + j],
                'embedding': result.embeddings[j] 
            })
    return embeddings

# save_topics_embeddings()
# load_topics_embeddings()