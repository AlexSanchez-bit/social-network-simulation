from src.nlp.similary import load_topics_similary_matrix, save_topics_similary_matrix, save_topics_embeddings



print('Building topics embeddings...')
save_topics_embeddings()

print('Building coorelation matrix between topics embeddings...')
save_topics_similary_matrix()