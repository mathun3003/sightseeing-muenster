# -*- coding: utf-8 -*-
import tensorflow as tf
from tensorflow import keras


class EfficientNetB7:
    def __init__(self):
        self.base_model = tf.keras.applications.efficientnet_v2.EfficientNetV2S(input_shape=(224, 224, 3), include_top=False, weights="imagenet")
        self.model = tf.keras.Sequential([self.base_model, keras.layers.GlobalAveragePooling2D(), keras.layers.Dense(12, activation="softmax")])
        self.config = self.model.get_config()
        self.summary = self.model.summary()

    def compile_model(self):
        # freeze pretraind layers
        for layer in self.model.layers[:-1]:
            layer.trainable = False

        # optimizer
        opt = keras.optimizers.Adam(learning_rate=0.001)

        # compile model
        self.model.compile(loss="CategoricalCrossentropy", optimizer=opt, metrics=["accuracy"])
        return self.model
