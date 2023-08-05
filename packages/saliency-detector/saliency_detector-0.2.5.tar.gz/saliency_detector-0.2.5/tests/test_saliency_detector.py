#!/usr/bin/env python

"""Tests the saliency_detector class"""

from PIL import Image
import cv2
import pytest
from saliency_detector import SaliencyDetector


def test_saliency_detector(image_filepaths):
    """Sample pytest test function with the pytest fixture as an argument."""
    # imgs = [Image.open(image_filepath) for image_filepath in image_filepaths[:2]]
    imgs = [cv2.imread(str(path)) for path in image_filepaths[:2]]
    sal_det = SaliencyDetector(pretrained_resnet50_path='saliency_detector/dataset/pretrained/resnet50_caffe.pth',
                               pretrained_saldet_model_path='saliency_detector/results/run-1/models/final.pth')
    result1 = sal_det.solver.predict(imgs[0])
    result2 = sal_det.solver.predict(imgs[1])

    print('bye')
