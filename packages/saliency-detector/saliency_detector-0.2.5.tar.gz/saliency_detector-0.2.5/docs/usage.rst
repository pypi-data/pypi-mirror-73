=====
Usage
=====

A pretrained resnet50 model and Poolnet saliency detector model are needed for this package to work properly.  They can be downloaded from the following links.

* Resnet50 Model: `<https://drive.google.com/open?id=1Q2Fg2KZV8AzNdWNjNgcavffKJBChdBgy>`_
* Poolnet Model: `<https://drive.google.com/file/d/1sH5RKEt6SnG33Z4sI-hfLs2d21GmegwR/view>`_

Extract the .pth files afterwards, and pass in the locations when instantiating the SaliencyDetector object.

.. code-block:: python3

    from saliency_detector import SaliencyDetector
    sal_det = SaliencyDetector(pretrained_resnet50_path='mypath_to/resnet50_caffe.pth',
                               pretrained_saldet_model_path='mypath_to/final.pth')
    result1 = sal_det.solver.predict(img[0])
    result2 = sal_det.solver.predict(img[1])

. . . etc.

