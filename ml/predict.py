# python 3.7.4
# coding = utf-8
# filename predict.py
# author 463714869@qq.com, create by VIM at 2019/11/6

from __future__ import absolute_import, division, print_function, unicode_literals

import tensorflow as tf
import cv2 as cv
from align import get_major_face_box
from datasets import prewhiten
import numpy as np


def getface(img_path, img_size, cv_model_path):
    img = cv.imread(img_path)
    classifier = cv.CascadeClassifier(cv_model_path)
    faceRect = classifier.detectMultiScale(img, scaleFactor=1.2, minNeighbors=3, minSize=(32, 32))
    if len(faceRect) > 0:
        majorFaceIndex = get_major_face_box(faceRect)
    else:
        print('Image %s not found any face\n' % img_path)
        exit(1)
    majorFace = faceRect[majorFaceIndex]
    img_cropped = img[majorFace[1]:majorFace[3] + 50, majorFace[0]:majorFace[2] + 50, :]
    try:
        scaled = cv.resize(img_cropped, (img_size, img_size), interpolation=cv.INTER_NEAREST)
    except:
        print('Image %s resize error, ignore\n' % img_path)
        exit(1)
    return scaled


if __name__ == '__main__':
    IMGS = 'D:\\BaiduNetdiskDownload\\FaceAttr\\UTKFace\\UTKFace\\28_1_1_20170117020409415.jpg'
    #MODEL_PATH = 'C:\\Users\\Admin\\Documents\\ZCIT-Projects\\PythonProj\\FaceAttr\\' \
    #             'models\\resnet50v2_b128_1e-3_20191214-164919\\face_attr_best.h5'
    MODEL_PATH = 'C:\\Users\\Admin\\Documents\\ZCIT-Projects\\PythonProj\\FaceAttr\\' \
                 'models\\resnet50v2_b128_1e-3_20191212-142111\\face_attr_best.h5'
    IMAGE_SIZE = 128

    imgs = [prewhiten(cv.resize(cv.imread(IMGS), (IMAGE_SIZE, IMAGE_SIZE), interpolation=cv.INTER_NEAREST))]
    imgs = np.stack(imgs)

    model = tf.keras.models.load_model(MODEL_PATH, compile=False)
    p = model.predict(imgs)

    age = np.sum(np.multiply(p[1][0], np.arange(101)))

    print(p[0])
    print(len(p[1][0]))
    print(list(p[1][0]).index(max(p[1][0])))
    print(max(p[1][0]))
    print(age)
    print(p[2])
