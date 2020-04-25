# python 3.7.4
# coding = utf-8
# filename train.py
# author 463714869@qq.com, create by VIM at 2019/11/5

from __future__ import absolute_import, division, print_function, unicode_literals

import os
import tensorflow as tf
from datetime import datetime
from ml import model as md
from ml import datasets

TRAIN_BATCH_SIZE = 10
TRAIN_EPOCHS = 50
MODEL_BASE_DIR = 'C:\\Users\\Admin\\Documents\\ZCIT-Projects\\PythonProj\\Quantification\\ml\\models'
LOG_BASE_DIR = 'C:\\Users\\Admin\\Documents\\ZCIT-Projects\\PythonProj\\Quantification\\ml\\logs'
LEARNING_RATE = 0.001
DROP_PROB = 0.8
PREFIX = 'gru-10_5_8e-1_1e-3_'
TSCODE = '000004.SZ'
TIMESTEP = 5


def train(tscode, save=True, pred=False, x=None):
    subdir = PREFIX + datetime.strftime(datetime.now(), '%Y%m%d-%H%M%S')
    log_dir_today = os.path.join(os.path.expanduser(LOG_BASE_DIR), subdir)
    model_dir_today = os.path.join(os.path.expanduser(MODEL_BASE_DIR), subdir)
    if save:
        if not os.path.isdir(log_dir_today):
            os.makedirs(log_dir_today)
        if not os.path.isdir(model_dir_today):
            os.makedirs(model_dir_today)
        print('Model directory: %s' % model_dir_today)
        print('Log directory  : %s' % log_dir_today)
    # trained_best_model_save_to = os.path.join(model_dir_today, 'gru_best.h5')

    print('Load train and validation data...')
    _, _, seq_len, train_x, train_y, test_x, test_y = datasets.make_train_test_data_by_tscode(tscode, TIMESTEP)
    print('Train-x: %d, train-y: %d' % (len(train_x), len(train_y)))
    print('Test-x: %d, test-y: %d' % (len(test_x), len(test_y)))

    print('Create model...')
    model = md.create_model(inp_shape=(TIMESTEP, seq_len), gru_units=seq_len + 1, dropout=DROP_PROB)

    print('Callbacks for tensorboard...')
    # tb = tf.keras.callbacks.TensorBoard(log_dir=log_dir_today, histogram_freq=1, write_images=True)
    # st = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=9)
    # cp = tf.keras.callbacks.ModelCheckpoint(trained_best_model_save_to, monitor='val_loss', save_best_only=True)
    rr = tf.keras.callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=3, min_lr=1e-6, verbose=0)

    print('Compile model...')
    model.compile(optimizer='Adam', loss='MSE', learning_rate=LEARNING_RATE)

    print('Train model with args...')
    h = model.fit(x=train_x, y=train_y, verbose=1, shuffle=False,
                  batch_size=TRAIN_BATCH_SIZE, epochs=TRAIN_EPOCHS,
                  validation_data=(test_x, test_y), callbacks=[rr])

    end_save_to = os.path.join(model_dir_today, 'gru_end.h5')
    if save:
        print('Done, save model to: %s' % end_save_to)
        model.save(end_save_to)

    p = 0.0
    if pred and x is not None:
        p = model.predict(x)[0]

    return end_save_to, p


if __name__ == '__main__':
    e, t = train(TSCODE)
    print(e)
    print(t)
