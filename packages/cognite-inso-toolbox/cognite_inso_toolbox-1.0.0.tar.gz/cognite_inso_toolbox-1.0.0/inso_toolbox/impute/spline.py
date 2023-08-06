import warnings

import pandas as pd

from inso_toolbox.utils.helpers import check_uniform


def impute_spline(data: pd.DataFrame, order: int = 1) -> pd.DataFrame:
    """ Spline imputation for time series data.

    Args:
        data (pandas.DataFrame): Time series to interpolate. Object must have datetime-like index.

    Returns:
        pandas.DataFrame: Uniform time series imputed with spline.
    """  # noqa
    # Check for empty time series
    if len(data) == 0:
        warnings.warn("The time series is empty.", RuntimeWarning)
        return data

    # Check if all values are NaN
    if data.isnull().all().value:
        warnings.warn("All values in the time series are NaN.", RuntimeWarning)
        return data

    # Check if initial value is NaN
    if pd.isna(data.iloc[0]).value:
        warnings.warn(
            "Initial value(s) in the time series are NaN. These initial value(s) will not be imputed.\n",
            RuntimeWarning,
            stacklevel=2,
        )

    # Check for uniformity
    if not check_uniform(data):
        warnings.warn("Time series is not uniform. This is required for correct linear imputation.", RuntimeWarning)

    # If NaNs are present, the number of datapoints has to be greater than the order of the polynomial
    # This is required in order to set up a well defined system of equations to calculate the coefficients
    if data.isna().any().value and (len(data) - data.isna().sum().value) <= order:
        raise ValueError(
            "To use a polynomial of order {} the number of non NaN values must be greater than the order.\n \
            There are currently {} non null values in the time series.\n".format(
                order, len(data) - data.isna().sum().value
            )
        )

    return data.interpolate(method="spline", limit_direction="forward", order=order)
