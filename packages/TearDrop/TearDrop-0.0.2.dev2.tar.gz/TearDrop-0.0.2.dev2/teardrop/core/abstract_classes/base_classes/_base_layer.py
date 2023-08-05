from abc import ABCMeta


class Layer(metaclass=ABCMeta):

    def _forward(self, X):
        raise NotImplementedError("Unfortunately, the function hasn't been added yet.")

    def initialize(self, neurons):
        raise NotImplementedError("Unfortunately, the function hasn't been added yet.")

    def _backward(self, last_derivative, lr, optimizer):
        raise NotImplementedError("Unfortunately, the function hasn't been added yet.")
