#Tensorflow implementation of representational learning to information extraction using subclassing
#This solution is presented as exact implementation mentioned in google's research paper, 
#If something feels wrong or some improvement, please do contact me at ayushpanwar691@gmail.com, 
#I am always available and much interested on improving this machine learning model implementation.   
#N=> number of neighbouring words of a candidate (Example: 10 )
#d=> embedding dimension size (Example: 100 dimensional vector=[1,2,1....3])
import tensorflow as tf
class Model(tf.keras.Model):
    def __init__(self, vocab_size, embedding_dimension, neighbours, heads):
        super().__init__()
        self.embedding_dimension = embedding_dimension
        self.dropout = 0.3
        # Neighbour position encoding must be done through non linear
        # positional embedding consisting of two RELU activated layers with dropout
        self.embed_neighbour = tf.keras.layers.Embedding(vocab_size, embedding_dimension)
        self.embed_neighbour_position_layer1=tf.keras.layers.Dense(embedding_dimension//2, activation='relu')
        self.dropout_neighbour_position_layer1=tf.keras.layers.Dropout(rate=self.dropout)
        self.embed_neighbour_position_layer2=tf.keras.layers.Dense(embedding_dimension, activation='relu')
        self.dropout_neighbour_position_layer2=tf.keras.layers.Dropout(rate=self.dropout)
        # Multihead attention done to scatter weights among neighbours, such that important
        # encoding weights are more considered of the neighbourhood encodings.
        self.multi_head_attention=tf.keras.layers.MultiHeadAttention(heads,embedding_dimension*2)
        # Each neighour embedding then projected from 2d to higher dimensions by a factor of 4
        self.project_2Nd_to_8Nd=tf.keras.layers.Dense(8*embedding_dimension, activation='relu')
        # Each neighbour embedding then projected back down to 2d to refine them.
        self.project_to_2Nd = tf.keras.layers.Dense(2*embedding_dimension)
        # Max pooling layer for neighborhood embedding to convert N*2d embedding to 2d.
        self.max_pool= tf.keras.layers.MaxPool1D(pool_size=neighbours,strides=neighbours)
        # Candidate position embedding is to be found through linear layer 
        self.embed_candidate_position= tf.keras.layers.Dense(embedding_dimension,'relu')
        # concatenate max pooled 2d embedding with candidate position 1d embedding to form  
         # 3d embedding and project down to 1d embedding with relu activated linear layer
        self.project_3d_to_1d=tf.keras.layers.Dense(embedding_dimension,activation='relu')
        # Compute field embedding through linear layer(TODO ALTHOUGH SINGLE NEURON 
        # IS USED, MULTI LAYER PERCEPTRON EMBEDDING IS PREFFERED)
        self.embed_field_id = tf.keras.layers.Dense(embedding_dimension, activation='relu')
        # Find Cosine similarity between field embedding and candidate embedding
        self.cosine_similarity = tf.keras.losses.CosineSimilarity(axis=1, reduction='none')
        # Compute Sigmoid
        self.sigmoid=tf.keras.layers.Dense(1,activation='sigmoid')
    def call(self, inputs):
        field_id, candidate, neighbour_words, neighbour_positions, masks=inputs
        batch_size=tf.shape(field_id)[0]
        neighbour_word_embeddings = self.embed_neighbour(neighbour_words) # (batch size,Nx1)=>(batch size,Nxd) 
        embed_neighbour_position_layer=self.embed_neighbour_position_layer1(neighbour_positions)
        dropout_neighbour_position_layer=self.dropout_neighbour_position_layer1(embed_neighbour_position_layer)
        embed_neighbour_position_layer=self.embed_neighbour_position_layer2(dropout_neighbour_position_layer)
        #(batch size,Nx2)=>(batch size,Nxd)
        neighbour_position_embeddings=self.dropout_neighbour_position_layer2(embed_neighbour_position_layer)
        # Concatenating neighbour and it's position embeddings   
        neighbour_embeddings = tf.concat([neighbour_word_embeddings, neighbour_position_embeddings], axis=2) # (Batch size,N x 2d)
        # Attention encodings (Batch size,N x 2d)
        attention= self.multi_head_attention(neighbour_embeddings, neighbour_embeddings,neighbour_embeddings) 
        # (Batch size,N x 8d) projected encodings
        projected_8Nd_encodings=self.project_2Nd_to_8Nd(attention)
        # (Batch size,N x 2d) projected encodings
        projected_2Nd_encodings=self.project_to_2Nd(projected_8Nd_encodings)
        # Flatten the 2d encodings for max pooling  (Batch size,N x 2d)   
        projected_2Nd_encodings= tf.reshape(projected_2Nd_encodings, [batch_size,-1,1])
        # Apply Max pool layer (Batch size,2d)
        max_pooled=tf.reshape(self.max_pool(attention),[batch_size,-1])  
        # get candidate position embedding  (Batch size,d)
        candidate_position_embedding= self.embed_candidate_position(candidate)
        # Concatenate candidate position embedding and max_pooled neighbour embedding (Batch size, 3d)
        concat=tf.reshape(tf.concat([candidate_position_embedding, max_pooled], axis=1),[batch_size,3*self.embedding_dimension])
        # Re-projecting concatenated embedding to (Batch size,d)
        projected_candidate_embedding = self.project_3d_to_1d(concat)
        # obtain d dimension field embedding (Batch size, d) 
        field_id_embedding = self.embed_field_id(tf.expand_dims(field_id, axis=-1))
        # obtain cosine similarity [-1,1] , (Batch size, 1)
        cosine_similarity = self.cosine_similarity(field_id_embedding, projected_candidate_embedding)
        return (cosine_similarity+1)/2
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    