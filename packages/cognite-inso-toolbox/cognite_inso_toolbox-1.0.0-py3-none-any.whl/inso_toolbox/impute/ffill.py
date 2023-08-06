import warnings
from typing import Union

import pandas as pd

from inso_toolbox.utils.helpers import check_uniform, is_na_all, is_na_initial


def impute_ffill(data: Union[pd.DataFrame, pd.Series]) -> Union[pd.DataFrame, pd.Series]:
    """ Forward fill imputation for time series data.

    Args:
        data (pd.DataFrame or pd.Series): Time series to impute.

    Returns:
        pd.DataFrame or pd.Series: Time series imputed with forward filling in time, with the original timestamps.
    """  # noqa
    # Only Pandas Series and DataFrame are supported
    assert isinstance(data, pd.Series) or isinstance(data, pd.DataFrame)

    # Check for empty time series
    if len(data) == 0:
        warnings.warn("The time series is empty.", RuntimeWarning)
        return data

    # Check if all values are NaN
    if is_na_all(data):
        warnings.warn("All values in the time series are NaN.", RuntimeWarning)
        return data

    # Check if initial value is NaN
    if is_na_initial(data):
        warnings.warn(
            "Initial value(s) in the time series are NaN. These initial value(s) will not be imputed.", RuntimeWarning
        )

    # Check for uniformity
    if not check_uniform(data):
        warnings.warn("Time series is not uniform. Forward fill imputation does not make it uniform.", RuntimeWarning)

    # Return interpolated data
    return data.fillna(method="ffill")
