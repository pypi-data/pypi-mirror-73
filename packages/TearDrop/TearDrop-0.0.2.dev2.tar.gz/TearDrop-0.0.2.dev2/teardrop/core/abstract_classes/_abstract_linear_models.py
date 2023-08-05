import numpy as np

from teardrop.core.abstract_classes.base_classes._base_linear_model import Linear
from teardrop.core.regression_results import RegressionResults


class LinearModel(Linear):

    def fit(self, x, y):
        # TODO: Add checks and more tests for linear models to make sure it catches wrong data.

        x_mean = np.mean(x)
        y_mean = np.mean(y)

        n = len(x)
        numerator = 0
        denominator = 0

        for point in range(n):
            numerator += np.multiply(x[point] - x_mean, y[point] - y_mean)
            denominator += np.square(x[point] - x_mean)

        b1 = np.divide(numerator, denominator)
        b0 = y_mean - np.multiply(b1, x_mean)

        reg = RegressionResults(b0, b1)

        return reg
