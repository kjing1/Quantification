# python 3.7.4
# coding = utf-8
# filename train.py
# author 463714869@qq.com, create by VIM at 2019/11/5

from __future__ import absolute_import, division, print_function, unicode_literals

import os
import tensorflow as tf
from datetime import datetime
from model import build_model, my_mae_accuracy
import datasets

TRAIN_BATCH_SIZE = 128
TRAIN_EPOCHS = 100
MODEL_BASE_DIR = 'C:\\Users\\Admin\\Documents\\ZCIT-Projects\\PythonProj\\FaceAttr\\models'
LOG_BASE_DIR = 'C:\\Users\\Admin\\Documents\\ZCIT-Projects\\PythonProj\\FaceAttr\\logs'
TRAIN_PROFILE = 'C:\\Users\\Admin\\Documents\\ZCIT-Projects\\PythonProj\\FaceAttr\\datasets\\train_profile.txt'
TEST_PROFILE = 'C:\\Users\\Admin\\Documents\\ZCIT-Projects\\PythonProj\\FaceAttr\\datasets\\test_profile.txt'
LEARNING_RATE = 0.00001
IMG_WIDTH = 128
IMG_HEIGHT = 128
IMG_CH = 3
DROP_PROB = 0.5
AGE_CLASSES = 100
GENDER_CLASSES = 2
SCORE_CLASSES = 1
PREFIX = 'resnet50v2_b128_1e-3_'

if __name__ == '__main__':
    subdir = PREFIX + datetime.strftime(datetime.now(), '%Y%m%d-%H%M%S')
    log_dir_today = os.path.join(os.path.expanduser(LOG_BASE_DIR), subdir)
    if not os.path.isdir(log_dir_today):
        os.makedirs(log_dir_today)
    model_dir_today = os.path.join(os.path.expanduser(MODEL_BASE_DIR), subdir)
    if not os.path.isdir(model_dir_today):
        os.makedirs(model_dir_today)
    print('Model directory: %s' % model_dir_today)
    print('Log directory  : %s' % log_dir_today)
    trained_best_model_save_to = os.path.join(model_dir_today, 'face_attr_best.h5')

    print('Load train and validation data...')
    train_x, train_gender_y, train_age_y, train_score_y = datasets.prepare_dataset(TRAIN_PROFILE)
    test_x, test_gender_y, test_age_y, test_score_y = datasets.prepare_dataset(TEST_PROFILE)
    print('Train data: %d, max age: %d' % (len(train_x), max(train_age_y)))
    print('Test data: %d, max age: %d' % (len(test_x), max(test_age_y)))

    train_ds = datasets.create_inputs(train_x, train_gender_y, train_age_y, train_score_y,
                                      batch_size=TRAIN_BATCH_SIZE, train=True)
    test_ds = datasets.create_inputs(test_x, test_gender_y, test_age_y, test_score_y,
                                     batch_size=TRAIN_BATCH_SIZE, train=False)

    print('Create model...')
    model = build_model(inp_shape=(IMG_WIDTH, IMG_HEIGHT, IMG_CH),
                        age_classes=AGE_CLASSES + 1,
                        gender_classes=GENDER_CLASSES,
                        cnn_layer_tobe_trainable=[], use_imagenet=True,
                        age_dense_trainable=True,
                        gender_dense_trainable=True,
                        score_dense_trainable=True)

    print('Callbacks for tensorboard...')
    tb = tf.keras.callbacks.TensorBoard(log_dir=log_dir_today, histogram_freq=1, write_images=True)
    st = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=9)
    cp = tf.keras.callbacks.ModelCheckpoint(trained_best_model_save_to, monitor='val_loss', save_best_only=True)
    rr = tf.keras.callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=3, min_lr=1e-6, verbose=0)
    # acc_save = SaveModelAccuracy(model_dir_today)

    losses = {
        'age_prob': 'sparse_categorical_crossentropy',
        'gender_prob': 'sparse_categorical_crossentropy',
        'score': 'MSE'
    }
    mts = {
        'age_prob': 'accuracy',
        'gender_prob': 'accuracy',
        'score': my_mae_accuracy
    }

    print('Compile model...')
    model.compile(optimizer='Adam', loss=losses, metrics=mts,
                  learning_rate=LEARNING_RATE)

    print('Train model with args...')
    h = model.fit(train_ds, epochs=TRAIN_EPOCHS, validation_data=test_ds, callbacks=[tb, cp, rr, st],
                  steps_per_epoch=int(len(train_x) / TRAIN_BATCH_SIZE))

    print('Done, save model to: %s' % os.path.join(model_dir_today, 'face_attr_end_train.h5'))
    model.save(os.path.join(model_dir_today, 'face_attr_end_train.h5'))
