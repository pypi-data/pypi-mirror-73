import warnings

import pandas as pd

from inso_toolbox.utils.helpers import check_uniform


def impute_mode(data: pd.DataFrame) -> pd.DataFrame:
    """ Mode imputation for time series data.

    Args:
        data (pandas.DataFrame): Time series to interpolate. Object must have datetime-like index.

    Returns:
        pandas.DataFrame: Uniform time series imputed with mode.
    """  # noqa
    # Check for empty time series
    if len(data) == 0:
        warnings.warn("The time series is empty.", RuntimeWarning)
        return data

    # Check if all values are NaN
    if data.isnull().all().value:
        warnings.warn("All values in the time series are NaN.", RuntimeWarning)
        return data

    # Check for uniformity
    if not check_uniform(data):
        warnings.warn("Time series is not uniform. This is required for correct linear imputation.", RuntimeWarning)

    modes = data.mode(axis=0, dropna=True)
    data = data.fillna(value=modes.iloc[0], axis=0)

    # Return filled data
    return data
