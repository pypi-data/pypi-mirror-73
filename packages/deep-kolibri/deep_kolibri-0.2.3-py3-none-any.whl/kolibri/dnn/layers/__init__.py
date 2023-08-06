# encoding: utf-8

# author: BrikerMan
# contact: eliyar917@gmail.com
# blog: https://eliyar.biz

# file: __init__.py
# time: 2019-05-23 14:05

from tensorflow.python import keras

from kolibri.dnn.layers.att_wgt_avg_layer import AttentionWeightedAverage, AttWgtAvgLayer
from kolibri.dnn.layers.att_wgt_avg_layer import AttentionWeightedAverageLayer
from kolibri.dnn.layers.folding_layer import FoldingLayer
from kolibri.dnn.layers.kmax_pool_layer import KMaxPoolingLayer, KMaxPoolLayer, KMaxPooling
from kolibri.dnn.layers.non_masking_layer import NonMaskingLayer

L = keras.layers

if __name__ == "__main__":
    print("Hello world")
