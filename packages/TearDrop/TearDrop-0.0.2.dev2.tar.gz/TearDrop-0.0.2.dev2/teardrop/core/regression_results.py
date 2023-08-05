from teardrop.core.abstract_classes.base_classes._base_linear_output import Output


class RegressionResults(Output):

    """
    RegressionResults class contains all necessary data returned after fitting LinearRegression model.

    Methods
    -------
    score
        Method which returns accuracy of fitted model.

    predict
        Function which allows you to predict next point on y-axis basing on x input.

    Attributes
    ----------
    b0: float, np.ndarray, int
        Contains intercept of the line returned by LinearRegression model.

    b1: float, np.ndarray, int
        Contains slope of the line returned by LinearRegression model.
    """

    def __init__(self, b0, b1):
        super().__init__(b0, b1)

    def score(self, x, y, threshold=0.95):

        """
        Parameters
        -----------
        x: array-like, list, tuple
            The point in x-axis used to predict the point in y-axis.

        y: array-like, list, tuple
            The correct point in y-axis which has to be predicted by the model.

        threshold: float, int
            The threshold which model's prediction has to fit to be called correct.
            When checking if prediction is correct, model checks if it fits between :math: +- y_j * threshold

        Returns
        --------
        accuracy: float, int
            The accuracy of the model.

        Raises
        ------
        ValueError
            When shape of `x` is not the same as shape of `y`.

        TypeError
            When `x` or `y` is not a :obj:`list` or :obj:`np.ndarray`
        """

        accuracy = super().score(x, y, threshold)
        return accuracy

    def predict(self, x):

        """
        Parameters
        ------------
        x: array-like, int, float
            Point in x-axis for which RegressionOutput class will predict point in y-axis.

        Returns
        ---------
        result: array-like, int, float
            Point in y-axis for which x was specified.

        Raises
        ------
        ValueError
            When `x`'s shape is not correct.
        """

        result = super().predict(x)
        return result

    @property
    def coeffs(self):

        """
        Returns
        -------
        coefficients: array-like, int, float
            Tuple containing model's coefficients `(b1, b0)`.
        """

        coefficients = super().coeffs
        return coefficients
