from typing import Union

import numpy as np

from teardrop.core.abstract_classes._abstract_linear_models import LinearModel
from teardrop.core.regression_results import RegressionResults


class LinearRegression(LinearModel):

    """LinearRegression model used for performing linear regression.

    Model used for linear regression.

    Methods
    -------
    fit
        Method used for fitting model and getting right coefficients.

    Example
    -------
    >>> from teardrop.linear_models import LinearRegression
    >>> import numpy as np
    >>> model = LinearRegression()
    >>> x = np.array([0, 1, 1])
    >>> y = np.array([1, 0, 0])
    >>> model.fit(x, y).coeffs
    (-1.0, 1.0)
    """

    def fit(
            self,
            x: Union[list, np.ndarray],
            y: Union[list, np.ndarray]
    ) -> RegressionResults:

        """
        Parameters
        -----------
        x: array-like
            The array containing data about x-axis used for fitting.

        y: array-like
            The array containing data about y-axis used for fitting.

        Returns
        ---------
        reg: RegressionOutput :obj:`teardrop.core.basic_linear_model.RegressionOutput`
            Object containing coefficients used for predicting and checking accuracy.

        See also
        ---------
        teardrop.core.regression_output.RegressionResults
        """

        reg = super().fit(x, y)
        return reg
