import tensorflow as tf

class NeighbourEmbedding(tf.keras.layers.Layer):
    def __init__(self, vocab_size, dimension):
        super(NeighbourEmbedding, self).__init__()
        self.word_embed = tf.keras.layers.Embedding(vocab_size, dimension)

        self.dropout = 0.3
        self.model = tf.keras.Sequential()
        self.num_layers=2
        for i in range(self.num_layers):
            units = dimension//self.num_layers
            if i == self.num_layers-1:
                units = dimension
            self.model.add(tf.keras.layers.Dense(units, activation='relu'))
            self.model.add(tf.keras.layers.Dropout(rate=self.dropout))


    def call(self, words, positions):
        # Word embedding
        embedding = self.word_embed(words)
        pos=self.model(positions)
        # Concatenating word and position embeddings
        neighbour_embedding = tf.concat([embedding, pos], axis=2)

        return neighbour_embedding
