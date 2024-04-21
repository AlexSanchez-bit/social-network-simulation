from src.nlp.similary import save_topics_correlation_matrix, save_topics_embeddings



print('Building topics embeddings...')
save_topics_embeddings()

print('Building coorelation matrix between topics embeddings...')
save_topics_correlation_matrix()