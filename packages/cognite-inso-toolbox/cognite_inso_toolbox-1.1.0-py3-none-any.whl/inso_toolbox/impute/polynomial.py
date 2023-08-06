import warnings
from typing import Union

import pandas as pd

from inso_toolbox.utils.helpers import check_uniform


def impute_polynomial(data: pd.DataFrame, order: int = 1, fill_last_values: Union[float, str] = None) -> pd.DataFrame:
    """ Polynomial imputation for time series data.
    Does not require uniform data for correct imputation.

    Args:
        data (pd.DataFrame): Time series to impute.
        order (int): Order of interpolating polynomial. Only odd degrees are supported (apart from degree 2).
        fill_last_values (float or "extrapolate"): Method for filling the last NaN values.

    Returns:
        pd.DataFrame: Inputed time series with same timestamps as the input time series.
    """  # noqa
    # Pandas interpolation only supports odd degrees or quadratic
    if order % 2 == 0 and order != 2:
        raise ValueError("Only odd degrees are supported for imputation (apart from quadratic).")

    # Check for empty time series
    if len(data) == 0:
        warnings.warn("The time series is empty.\n", RuntimeWarning, stacklevel=2)
        return data

    # Check if all values are NaN
    if data.isnull().all().value:
        warnings.warn("All values in the time series are NaN.\n", RuntimeWarning, stacklevel=2)
        return data

    # If NaNs are present, the number of datapoints has to be greater than the order of the polynomial
    # This is required in order to set up a well defined system of equations to calculate the coefficients
    if data.isna().any().value and (len(data) - data.isna().sum().value) <= order:
        raise ValueError(
            "To use a polynomial of order {} the number of non NaN values must be greater than the order.\n \
            There are currently {} non null values in the time series.\n".format(
                order, len(data) - data.isna().sum().value
            )
        )

    # Check if initial value is NaN
    if pd.isna(data.iloc[0]).value:
        warnings.warn(
            "Initial value(s) in the time series are NaN. These initial value(s) will not be imputed.\n",
            RuntimeWarning,
            stacklevel=2,
        )

    # Check if last value is NaN
    if pd.isna(data.iloc[-1]).value and fill_last_values is None:
        warnings.warn(
            "Last value(s) in the time series are NaN. These last value(s) will not be imputed.\n",
            RuntimeWarning,
            stacklevel=2,
        )

    # Check for uniformity
    if not check_uniform(data):
        warnings.warn(
            "Time series is not uniform. Imputed time series will have the same non uniform timestamps.\n",
            RuntimeWarning,
            stacklevel=2,
        )

    # Return the interpolated polynomial
    return data.interpolate(method="polynomial", limit_direction="forward", order=order, fill_value=fill_last_values)
