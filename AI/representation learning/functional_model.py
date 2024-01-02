# This is a functional implementation of information extraction from document 
# functional model is found to be better to save and load rather than class model version 
# hence made replica of class model in the form of function. 
import tensorflow as tf

def Model(vocab_size, embedding_dimension, neighbours, heads):
    # Input layers
    field_id = tf.keras.Input(shape=(1), dtype=tf.int32)
    candidate = tf.keras.Input(shape=(2), dtype=tf.float32)
    neighbour_words = tf.keras.Input(shape=(neighbours), dtype=tf.int32)
    neighbour_positions = tf.keras.Input(shape=(neighbours,2), dtype=tf.float32)
    # Embedding layers
    neighbour_word_embeddings = tf.keras.layers.Embedding(vocab_size, embedding_dimension,mask_zero=True)(neighbour_words)
    neighbour_positions = tf.keras.layers.Masking(mask_value=[-1,-1])(neighbour_positions)    
    embed_neighbour_position_layer1 = tf.keras.layers.Dense(embedding_dimension // 2, activation='relu')(neighbour_positions)
    dropout_neighbour_position_layer1 = tf.keras.layers.Dropout(rate=0.2)(embed_neighbour_position_layer1)
    embed_neighbour_position_layer2 = tf.keras.layers.Dense(embedding_dimension, activation='relu')(dropout_neighbour_position_layer1)
    dropout_neighbour_position_layer2 = tf.keras.layers.Dropout(rate=0.2)(embed_neighbour_position_layer2)
    neighbour_position_embeddings = tf.concat([neighbour_word_embeddings, dropout_neighbour_position_layer2],axis=2)
    # Multi-head attention layer
    attention = tf.keras.layers.MultiHeadAttention(heads, embedding_dimension * 2)(neighbour_position_embeddings, neighbour_position_embeddings, neighbour_position_embeddings)

    # Dense layers
    projected_8Nd_encodings = tf.keras.layers.Dense(8 * embedding_dimension, activation='relu')(attention)
    projected_2Nd_encodings = tf.keras.layers.Dense(2 * embedding_dimension)(projected_8Nd_encodings)
    projected_2Nd_encodings = tf.keras.layers.Reshape([-1,1])(projected_2Nd_encodings)
    max_pooled =tf.keras.layers.MaxPool1D(pool_size=neighbours, strides=neighbours)(projected_2Nd_encodings)
    max_pooled=tf.squeeze(max_pooled, axis=2)
    candidate_position_embedding = tf.keras.layers.Dense(embedding_dimension)(candidate)
    concat = tf.concat([candidate_position_embedding, max_pooled],axis=1)
    projected_candidate_embedding = tf.keras.layers.Dense(embedding_dimension)(concat)
    field_id_embedding = tf.keras.layers.Dense(embedding_dimension)(field_id)
    # Cosine similarity layer
    cosine_similarity =  tf.keras.losses.CosineSimilarity(axis=-1,reduction='none')(field_id_embedding,projected_candidate_embedding)
    output=(cosine_similarity+1)/2
    return tf.keras.Model(inputs=[field_id, candidate, neighbour_words, neighbour_positions], outputs=output)
