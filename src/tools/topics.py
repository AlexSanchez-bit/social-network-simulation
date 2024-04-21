from ..tools.prompts import TopicRelevance
from ..nlp.similary import embed, load_topics_embeddings, cosine_distance
import numpy as np

def build_topics_relevances(main_topics: list[TopicRelevance]):    
    """Build the topics based in the mainly topics extracted from the user input"""
    # embeddings of all topics
    all_topics = load_topics_embeddings()
    n = len(all_topics)
    m = len(main_topics)
    # calculate the embedding representation of each one
    ai_topics = embed([t.topic for t in main_topics])
    
    # relevance of each topic on the network
    relevance = [] 
    for t in all_topics:
        rel = 0
        # average of the weighted sum to calculate topic[i] relevance
        for i, ait in enumerate(ai_topics):
            rel += (
                main_topics[i].relevance * cosine_distance(t['embedding'], ait['embedding'])
            )
        relevance.append(rel / m)
    
    return relevance
