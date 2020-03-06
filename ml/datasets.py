# python 3.7.4
# coding = utf-8
# filename datasets.py
# author 463714869@qq.com, create by VIM at 2019/11/5

from __future__ import absolute_import, division, print_function, unicode_literals

import numpy as np
import os
import tensorflow as tf
import multiprocessing as mt
import cv2


def prewhiten(x):
    mean = np.mean(x)
    std = np.std(x)
    std_adj = np.maximum(std, 1.0 / np.sqrt(x.size))
    y = np.multiply(np.subtract(x, mean), 1 / std_adj)
    return y


def _process_one_image(file_path):
    image_string = tf.io.read_file(file_path)
    image_decoded = tf.cond(
        tf.image.is_jpeg(image_string),
        lambda: tf.image.decode_jpeg(image_string, channels=3),
        lambda: tf.image.decode_png(image_string, channels=3))
    image_converted = tf.image.resize(image_decoded, [160, 160])
    # 随机剪裁
    image_converted = tf.image.random_crop(image_converted, size=[128, 128, 3])
    # 随机对比度
    image_converted = tf.image.random_contrast(image_converted, lower=0.2, upper=0.8)
    # 随机饱和度
    image_converted = tf.image.random_saturation(image_converted, lower=0.2, upper=0.8)
    # 随机镜像
    image_converted = tf.image.random_flip_left_right(image_converted)
    # 标准化
    image_converted = tf.image.per_image_standardization(image_converted)
    return image_converted


def _process_one_image_val(file_path):
    image_string = tf.io.read_file(file_path)
    image_decoded = tf.cond(
        tf.image.is_jpeg(image_string),
        lambda: tf.image.decode_jpeg(image_string, channels=3),
        lambda: tf.image.decode_png(image_string, channels=3))
    image_converted = tf.image.resize(image_decoded, [128, 128])
    image_converted = tf.image.per_image_standardization(image_converted)
    return image_converted


def prepare_dataset(profile):
    imgs_and_labels = []
    list_files = []
    age_labels = []
    gender_labels = []
    score_labels = []

    with open(profile, 'r') as f:
        cont = f.readlines()
        for line in cont:
            imgs_and_labels.append(line.replace('\n', '').split(' '))

    np.random.shuffle(imgs_and_labels)
    for l in imgs_and_labels:

        gender = int(float(l[1]))
        age = int(float(l[2]))
        score = round(float(l[3]), 2)
        score = score if score <= 5.0 else 5.0
        if age > 100 or gender not in [0, 1]:
            continue

        im = cv2.imread(l[0])
        if im is None:
            print('CV2 read image error, image is None, image is : %s' % l[0])
            continue
        if len(im.shape) != 3:
            print('Image %s not RGB, %d dims' % (l[0], len(im.shape)))
            continue
        if not os.path.exists(l[0]):
            print('Image %s not found, ignore' % l[0])
            continue

        list_files.append(l[0])
        gender_labels.append(gender)
        age_labels.append(age)
        score_labels.append(score)

    return list_files, gender_labels, age_labels, score_labels


def create_inputs(list_files, gender_labels, age_labels, score_labels, batch_size=128, train=True):
    ds_img = tf.data.Dataset.from_tensor_slices((tf.constant(list_files)))
    if train:
        ds_img = ds_img.map(_process_one_image, num_parallel_calls=mt.cpu_count())
    else:
        ds_img = ds_img.map(_process_one_image_val, num_parallel_calls=mt.cpu_count())
    ds_labels = tf.data.Dataset.from_tensor_slices((tf.constant(gender_labels),
                                                   tf.constant(age_labels), tf.constant(score_labels)))
    ds = tf.data.Dataset.zip((ds_img, ds_labels))
    ds = ds.batch(batch_size)
    if train:
        ds = ds.repeat()
    return ds


if __name__ == '__main__':
    imgs_and_labels = []
    with open("C:\\Users\\Admin\\Documents\\ZCIT-Projects\\PythonProj\\FaceAttr\\datasets\\train_wiki.txt", 'r') as f:
        cont = f.readlines()
        for line in cont:
            imgs_and_labels.append(line.replace('\n', '').split(' '))

    np.random.shuffle(imgs_and_labels)
    with open("C:\\Users\\Admin\\Documents\\ZCIT-Projects\\PythonProj\\FaceAttr\\datasets\\train_profile.txt", 'w') as train_wf:
        with open("C:\\Users\\Admin\\Documents\\ZCIT-Projects\\PythonProj\\FaceAttr\\datasets\\test_profile.txt", 'w') as test_wf:
            for i, l in enumerate(imgs_and_labels):
                if i % 5 == 0:
                    test_wf.write("%s %s %s %s\n" % (l[0], l[1], l[2], l[3]))
                else:
                    train_wf.write("%s %s %s %s\n" % (l[0], l[1], l[2], l[3]))
