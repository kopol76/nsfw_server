#!/usr/bin/env python
"""
Copyright 2016 Yahoo Inc.
Licensed under the terms of the 2 clause BSD license. 
Please see LICENSE file in the project root for terms.
"""
import random
import string

import numpy as np
import os
import sys

import glob
import time

from PIL import Image

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
from io import BytesIO

os.environ['GLOG_minloglevel'] = '2'
import caffe


def resize_image(img_data, sz=(256, 256)):
    im = Image.open(BytesIO(img_data))
    if im.mode != "RGB":
        im = im.convert("RGB")
    imr = im.resize(sz, resample=Image.BILINEAR)
    fh_im = BytesIO()
    imr.save(fh_im, format="JPEG")
    fh_im.seek(0)
    return bytearray(fh_im.read())

def caffe_preprocess_and_compute(pimg, caffe_transformer=None, caffe_net=None,
                                 output_layers=None):
    """
    Run a Caffe network on an input image after preprocessing it to prepare
    it for Caffe.
    :param PIL.Image pimg:
        PIL image to be input into Caffe.
    :param caffe.Net caffe_net:
        A Caffe network with which to process pimg afrer preprocessing.
    :param list output_layers:
        A list of the names of the layers from caffe_net whose outputs are to
        to be returned.  If this is None, the default outputs for the network
        are returned.
    :return:
        Returns the requested outputs from the Caffe net.
    """
    if caffe_net is not None:

        # Grab the default output names if none were requested specifically.
        if output_layers is None:
            output_layers = caffe_net.outputs

        img_data_rs = resize_image(pimg, sz=(256, 256))
        image = caffe.io.load_image(BytesIO(img_data_rs))

        H, W, _ = image.shape
        _, _, h, w = caffe_net.blobs['data'].data.shape
        h_off = int(max((H - h) / 2, 0))
        w_off = int(max((W - w) / 2, 0))

        crop = image[h_off:h_off + h, w_off:w_off + w, :]
        transformed_image = caffe_transformer.preprocess('data', crop)
        transformed_image.shape = (1,) + transformed_image.shape

        input_name = caffe_net.inputs[0]
        all_outputs = caffe_net.forward_all(blobs=output_layers,
                                            **{input_name: transformed_image})

        outputs = all_outputs[output_layers[0]][0].astype(float)
        return outputs
    else:
        return []


default_model = "nsfw_model/deploy.prototxt"
default_pretrained_model = "nsfw_model/resnet_50_1by2_nsfw.caffemodel"

def get_score_net(image_data, caffe_net, caffe_transformer):
    # Classify.
    scores = caffe_preprocess_and_compute(image_data, caffe_transformer=caffe_transformer, caffe_net=caffe_net,
                                          output_layers=['prob'])
    #print "NSFW score:  ", scores[1]

    return scores[1]

def load_model(model=default_model, pretrained_model=default_pretrained_model):
    # Pre-load caffe model.
    nsfw_net = caffe.Net(model,  # pylint: disable=invalid-name
                         pretrained_model, caffe.TEST)

    # Load transformer
    # Note that the parameters are hard-coded for best results
    caffe_transformer = caffe.io.Transformer({'data': nsfw_net.blobs['data'].data.shape})
    caffe_transformer.set_transpose('data', (2, 0, 1))  # move image channels to outermost
    caffe_transformer.set_mean('data', np.array([104, 117, 123]))  # subtract the dataset-mean value in each channel
    caffe_transformer.set_raw_scale('data', 255)  # rescale from [0, 1] to [0, 255]
    caffe_transformer.set_channel_swap('data', (2, 1, 0))  # swap channels from RGB to BGR

    return nsfw_net, caffe_transformer

