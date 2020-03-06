# python 3.7.4
# coding = utf-8
# filename model.py
# author 463714869@qq.com/www.cdzcit.com,
#        create by VIM at 2020/2/25

from __future__ import absolute_import, division, print_function, unicode_literals

from tensorflow.keras import layers, models
import tensorflow as tf
from tensorflow.keras.callbacks import Callback
import os


def build_model(inp_shape=(128, 128, 3),
                age_classes=100,
                gender_classes=2,
                cnn_layer_tobe_trainable=[],
                use_imagenet=True,
                age_dense_trainable=True,
                gender_dense_trainable=True,
                score_dense_trainable=True):
    img_inputs = tf.keras.Input(shape=inp_shape)
    if use_imagenet:
        base_model = tf.keras.applications.ResNet50(input_tensor=img_inputs,
                                                    weights='imagenet', include_top=False, pooling='avg')
        """
        # Layers in list to be trainable
        for layer in base_model.layers:
            if layer.name in cnn_layer_tobe_trainable:
                layer.trainable = True
            else:
                layer.trainable = False
        """
    else:
        base_model = tf.keras.applications.ResNet50V2(input_tensor=img_inputs,
                                                      weights=None, include_top=False, pooling='avg')

    gender_prob = layers.Dense(gender_classes, activation='softmax', name='gender_prob')(base_model.output)
    age_prob = layers.Dense(age_classes, activation='softmax', name='age_prob')(base_model.output)
    score = layers.Dense(1, name='score')(base_model.output)
    model = tf.keras.Model(inputs=img_inputs, outputs=[gender_prob, age_prob, score])

    for layer in model.layers[-3:]:
        if layer.name == 'age_prob':
            if not age_dense_trainable:
                layer.trainable = False
        elif layer.name == 'gender_prob':
            if not gender_dense_trainable:
                layer.trainable = False
        elif layer.name == 'score':
            if not score_dense_trainable:
                layer.trainable = False
        else:
            raise Exception("Unkown layer", layer.name)

    model.summary()
    return model


def my_mae_accuracy(y_true, y_pred):
    y_true_covt = tf.cast(y_true, tf.int32)
    y_pred_covt = tf.cast(y_pred, tf.int32)
    acc = tf.math.reduce_mean(tf.cast(tf.math.equal(y_true_covt, y_pred_covt), tf.float32))
    return acc


class SaveModelAccuracy(Callback):
    def __init__(self, savedir='.'):
        self.model_save_to = savedir
        self.max_acc = 0.8

    def on_epoch_end(self, epoch, logs={}):
        logs = logs or {}
        max_accuracy_epoch = logs.get('val_accuracy')
        if max_accuracy_epoch > self.max_acc:
            to = os.path.join(self.model_save_to, 'max_accuray-epoch%d-%.2f.h5' % (epoch, max_accuracy_epoch))
            self.model.save(to)
            self.max_acc = max_accuracy_epoch
            print('\nModel save to %s, accuray is %.2f' % (to, max_accuracy_epoch))
