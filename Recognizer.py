import tensorflow as tf
probability_model = tf.keras.Sequential([tf.keras.models.load_model("MNIST-AI.h5"), tf.keras.layers.Softmax()])