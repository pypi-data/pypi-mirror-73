from abc import ABCMeta

import numpy as np

from teardrop.data_tools import load_headbrain


class Linear(metaclass=ABCMeta):

    def fit(self, x, y):
        pass
