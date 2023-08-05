from typing import Union

import numpy as np

from teardrop.core.abstract_classes._abstract_optimizers import AbstractSGD


class SGD(AbstractSGD):

    """Stochastic gradient descent algorithm class.

    Class used for initializing SGD for ``Sequential`` model

    Methods
    -------
    update
        Updates passed gradient.

    Example
    -------
    >>> import numpy as np
    >>> from teardrop.optimizers import SGD
    >>> sgd = SGD()
    >>> gradient = np.array([2.23, 1.21, 4.123])
    >>> learning_rate = 0.01
    >>> sgd.update(gradient, learning_rate)
    array([0.0223 , 0.0121 , 0.04123])

    See also
    --------
    teardrop.neural_networks.Sequential

    """

    def update(
            self,
            gradient: Union[list, np.ndarray],
            lr: Union[int, float]
    ):
        """
        Parameters
        -----------
        gradient: array-like
            The array with gradient already changed to update weights.

        lr: float or int
            The "length" of the step in updating weights.

        Returns
        --------
        change: array-like
            The gradient used in back propagation.
        """

        change = super().update(gradient, lr)
        return change
