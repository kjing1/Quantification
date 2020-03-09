# python 3.7.4
# coding = utf-8
# filename model.py
# author 463714869@qq.com, create by VIM at 2019/10/16

from __future__ import absolute_import, division, print_function, unicode_literals

import tensorflow as tf
from tensorflow.keras import layers, models
import tensorflow.keras.backend as K
from tensorflow.keras.callbacks import Callback, TensorBoard
from tensorflow.keras.regularizers import l2
import os
import numpy as np


def create_base_model(inp_shape=(300, 10), gru_units=512, dropout=0.2):
    img_inputs = tf.keras.Input(name='stocks_inputs', shape=inp_shape)

    x = layers.Bidirectional(layers.GRU(gru_units, return_sequences=True))(img_inputs)
    x = layers.Bidirectional(layers.GRU(gru_units, return_sequences=True))(x)

    classes_prob = layers.Dense(1, activation='softmax', name='cls_prob')(x)
    model = tf.keras.Model(inputs=img_inputs, outputs=classes_prob)

    model.summary()

    return model
