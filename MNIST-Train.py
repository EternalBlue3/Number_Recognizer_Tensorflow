import os
os.environ['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION'] = 'python'

import numpy as np
import tensorflow as tf
from tensorflow import keras
from sklearn.model_selection import train_test_split

def create_model():
    model = tf.keras.Sequential([
        keras.layers.Dense(512, activation='relu', input_shape=(784,)),
        keras.layers.Dropout(0.2),
        keras.layers.Dense(10)
    ])

    model.compile(optimizer='adam',loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),metrics=[tf.keras.metrics.SparseCategoricalAccuracy()])

    return model

(train_images, train_labels), (test_images, test_labels) = tf.keras.datasets.mnist.load_data()
train_images = train_images.reshape(-1, 784) / 255.0
test_images = test_images.reshape(-1, 784) / 255.0

# Define the model architecture and compile it
model = create_model()

# Train the model on the custom dataset
model.fit(train_images, train_labels, epochs=30, validation_data=(test_images, test_labels))

# Evaluate the model's performance on the custom dataset
loss, acc = model.evaluate(test_images, test_labels, verbose=2)
print("Model accuracy: {:5.2f}%".format(100 * acc))

# Save the model
model.save("MNIST-AI.h5")
