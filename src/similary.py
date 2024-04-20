import voyageai
import pickle
import json
from .constants import VOYAGE_API_KEY, VOYAGE_EMBED_BATCH_SIZE

def load_topics_embeddings():
    embeddings = pickle.load(open('./topic-embed.pkl', 'rb'))
    return embeddings

def save_topics_embeddings():
    vo = voyageai.Client(api_key=VOYAGE_API_KEY)

    # I assume the cosistency of the data
    with open('./data/topics.txt', 'r') as f:
        topics = f.read().split('\n')
        embeddings = []
        
        for i in range(0, len(topics), VOYAGE_EMBED_BATCH_SIZE):
            batch = topics[i:i+VOYAGE_EMBED_BATCH_SIZE]
            print(len(batch))
            result = vo.embed(batch, model='voyage-lite-02-instruct')
            print(result.total_tokens)
            
            for j in range(len(batch)):
                embeddings.append({
                    'topic': topics[i + j],
                    'embedding': result.embeddings[j] 
                })
                    
        pickle.dump(embeddings, open('./data/topic-embed.pkl', 'wb'))    
        with open('./data/topic-embed.json', 'w') as f:
            f.write(json.dumps(embeddings))
        
        
# save_topics_embeddings()
# load_topics_embeddings()