import tensorflow as tf

def load_model():
    recognizer = tf.keras.models.load_model("Digits_Recognizer")
    probability_model = tf.keras.Sequential([recognizer, tf.keras.layers.Softmax()])
    return probability_model
