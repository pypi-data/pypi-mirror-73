from pathlib import Path
from collections import namedtuple
import torch

from saliency_detector.dataset.joint_dataset import get_loader
from saliency_detector.joint_solver import Solver

__version__ = "0.2.5"

config_attr_defaults = {'cuda': None,
                        'mode': 'test',
                        'model': None,
                        'test_mode': 1,
                        'num_thread': 0,
                        'image_paths': None,
                        'test_list': None,
                        'test_loader': None,
                        'batch_size': 1,
                        'arch': 'resnet',
                        'load': '',
                        'pretrained_model': None}

Config = namedtuple('Config', config_attr_defaults.keys(), defaults=config_attr_defaults.values())


class SaliencyDetector():
    def __init__(self, pretrained_resnet50_path, pretrained_saldet_model_path, cuda=None):
        """

        Parameters
        ----------
        pretrained_resnet50_path: Path or string
        pretrained_saldet_model_path: Path or string
        cuda: bool
        """
        if cuda is None:
            # autodetect if gpu is available, if not specified
            cuda = True if torch.cuda.is_available() else False


        self.config = Config(cuda=cuda, mode='test', num_thread=0, image_paths=None, test_list=None,
                             model=str(pretrained_saldet_model_path), pretrained_model=str(pretrained_resnet50_path))
        # test_loader = get_loader(self.config, mode='test')
        # self.config._replace(test_loader=test_loader)

        self.solver = Solver(None, test_loader=None, config=self.config)
        # self.solver_iter = iter(self.solver)

    def __iter__(self):
        self.solver.iter = iter(self.solver)
        return self

    def __next__(self):
        return next(self.solver.iter)

    # def predict_next(self):
    #     return next(self.solver_iter)
    #
    # def predict_all(self):
    #     salient_map_images = [im for im in self.solver]
    #     return salient_map_images


    def reset_iterator(self):
        self.solver.iter = iter(self.solver)
