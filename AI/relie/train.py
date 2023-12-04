import tensorflow as tf
import numpy as np
import warnings
from generator import Generator
warnings.filterwarnings("ignore")
gen=Generator()   
from model import Model
gen.generate_data()
y_train=tf.constant(gen.ground_truth)
cand_pos=tf.constant(gen.cand_pos)
neighbours=tf.constant(gen.neighbours)
neighbour_positions=tf.constant(gen.neighbours_pos)
field_id=tf.constant(gen.field)
masks=tf.constant(gen.masks)
VOCAB_SIZE=2000
EMBEDDING_SIZE=100
NEIGHBOURS=10
HEADS=4
model = Model(VOCAB_SIZE, EMBEDDING_SIZE, NEIGHBOURS, HEADS)
model.compile(
optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
loss=tf.keras.losses.BinaryCrossentropy(),
metrics=[tf.keras.metrics.BinaryAccuracy(),
         tf.keras.metrics.Precision(thresholds=0.5),
         tf.keras.metrics.Recall(thresholds=0.5)])

model.fit((field_id,cand_pos,neighbours,neighbour_positions,masks),y_train,epochs=100)
model.save('model.keras')