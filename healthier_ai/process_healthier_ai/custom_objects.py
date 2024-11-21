import tensorflow as tf


@tf.keras.utils.register_keras_serializable()
def swish(x):
    return tf.nn.swish(x)


@tf.keras.utils.register_keras_serializable()
class FixedDropout(tf.keras.layers.Dropout):
    def __init__(self, rate, **kwargs):
        super().__init__(rate, **kwargs)

    def get_config(self):
        config = super().get_config()
        config.update({"rate": self.rate})
        return config

    def call(self, inputs, training=None):
        return super().call(inputs, training=True)  # Always apply dropout
