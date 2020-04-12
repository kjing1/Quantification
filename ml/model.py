# python 3.7.4
# coding = utf-8
# filename model.py
# author 463714869@qq.com, create by VIM at 2019/10/16

from __future__ import absolute_import, division, print_function, unicode_literals

import tensorflow as tf
from tensorflow.keras import layers, models


def create_model(inp_shape=(5, 19), gru_units=32, dropout=0.8):
    q_inputs = tf.keras.Input(name='q_inputs', shape=inp_shape)

    x = layers.Bidirectional(layers.GRU(gru_units, return_sequences=True))(q_inputs)
    x = layers.Dropout(dropout)(x)
    x = layers.Bidirectional(layers.GRU(gru_units, return_sequences=False))(x)
    x = layers.Dropout(dropout)(x)

    close = layers.Dense(1, activation='linear', name='close')(x)
    model = tf.keras.Model(inputs=q_inputs, outputs=close)

    model.summary()

    return model
