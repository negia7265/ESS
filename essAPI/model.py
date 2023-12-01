import tensorflow as tf 
from attention import MultiHeadAttention
from neigh import NeighbourEmbedding
class Model(tf.keras.Model):
    def __init__(self, vocab_size, embedding_dim, neighbours, heads):
        super().__init__()

        self.cand_embed = tf.keras.layers.Dense(embedding_dim, activation=tf.nn.relu)
        self.field_embed = tf.keras.layers.Dense(embedding_dim, activation=tf.nn.relu)
        self.embedding_dimension = embedding_dim
        self.neighbour_embeddings = NeighbourEmbedding(vocab_size, embedding_dim) 
        self.attention_encodings = MultiHeadAttention(heads, embedding_dim * 2)
        self.linear_projection_2 = tf.keras.layers.Dense(embedding_dim )
        # self.linear_projection = tf.keras.layers.Dense(8*embedding_dim,activation=tf.nn.relu)
         # Max pooling layer for neighborhood embedding
        self.max_pool = tf.keras.layers.MaxPool1D(pool_size=neighbours,strides=neighbours)
        self.cos_sim = tf.keras.losses.CosineSimilarity(axis=1, reduction='none')
    def call(self, inputs):
        field_id, candidate, neighbour_words, neighbour_positions, masks=inputs
        # Field and candidate embeddings
        id_embed = self.field_embed(tf.expand_dims(field_id, axis=-1))  
        cand_embed = self.cand_embed(candidate)
        # Neighbour embeddings
        neighbour_embeds = self.neighbour_embeddings(neighbour_words, neighbour_positions)
        # Attention encodings
        attention= self.attention_encodings(neighbour_embeds, neighbour_embeds, neighbour_embeds, mask=masks)         
        bs=tf.shape(attention)[0]
        # Linear projection of attention to concatenate with candidate embedding
        # linear_proj = tf.keras.activations.relu(self.linear_projection(attention))
        attention= tf.reshape(attention, [bs,-1,1])
        # Apply Max pool layer 
        max_pooled=tf.reshape(self.max_pool(attention),[bs,-1])  
        # Concatenating Candidate position embedding and max_pooled neighbour embedding
        concat = tf.concat([cand_embed, max_pooled], axis=1)
        concat=tf.reshape(concat,[bs,3*self.embedding_dimension])
        # Re-projecting concatenated embedding to calculate cosing similarity
        projected_candidate_encoding = tf.keras.activations.relu(self.linear_projection_2(concat))
        # Calculating cosine similarity and scaling to [0,1]
        similarity = self.cos_sim(id_embed, projected_candidate_encoding)
        scores = (similarity - 1) / 2
        return scores
