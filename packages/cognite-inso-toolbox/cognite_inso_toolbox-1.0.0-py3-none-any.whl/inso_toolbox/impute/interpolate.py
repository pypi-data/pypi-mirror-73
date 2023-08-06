import warnings
from datetime import datetime
from typing import Union

import numpy as np
import pandas as pd
import scipy.interpolate

from inso_toolbox.utils import pipeline_function
from inso_toolbox.utils.helpers import functional_mean, is_na_all


@pipeline_function
def interpolate(
    data: Union[pd.DataFrame, pd.Series],
    kind: str = "linear",
    method: str = "pointwise",
    granularity: str = "1s",
    start: Union[int, datetime] = None,
    end: Union[int, datetime] = None,
) -> Union[pd.DataFrame, pd.Series]:
    """ Approximates data using function, then interpolates for timestamps between start_date and end_date with specified frequency.
    
    Args:
        data (pd.DataFrame or pd.Series): Time series to impute.
        kind (str): Specifies the kind of interpolation (‘linear’, ‘nearest’, ‘zero’, ‘slinear’, ‘quadratic’,
            ‘cubic’, ‘previous’, ‘next’, where ‘zero’, ‘slinear’, ‘quadratic’ and ‘cubic’ refer to a spline
            interpolation of zeroth, first, second or third order; ‘previous’ and ‘next’ simply return the
            previous or next value of the point) 
        method (str): The kind of interpolation to perform. "pointwise" gets the exact value of the corresponding timestamp.
        granularity (str): frequency of output e.g. '1s' or '2h'
        start (optional int or datetime): Start datetime or timestamp of output dataframe
        end (optional int or datetime): End datetime or timestamp of output dataframe
        
    Returns:
        pd.DataFrame or pd.Series: Time series imputed with forward filling in time, with the original timestamps.
        
    """  # noqa
    # Only pd.Series and pd.DataFrame inputs are supported
    if not isinstance(data, pd.Series) and not isinstance(data, pd.DataFrame):
        raise ValueError("Only pd.Series and pd.DataFrame inputs are supported.")

    # Check for empty time series
    if len(data) == 0:
        warnings.warn("The time series is empty.", RuntimeWarning)
        return data

    # Check if all values are NaN
    if is_na_all(data):
        warnings.warn("All values in the time series are NaN.", RuntimeWarning)
        return data

    # Allow for other ways of defining forward filling for stepwise functions
    kind = "previous" if kind in ("ffill", "stepwise") else kind

    # Get start and end dates and store as datetime
    if not start:
        start = data.index[0]
    elif isinstance(start, int):
        # If milliseconds provided, recast to float as datetime will throw exception otherwise
        if len(str(start)) == 13:
            start = datetime.fromtimestamp(start / 1000)
        elif len(str(start)) == 10:
            start = datetime.fromtimestamp(start)
        else:
            raise ValueError("Start timestamp is outside valid range.")
    if not end:
        end = data.index[-1]
    elif isinstance(end, int):
        # If milliseconds provided, recast to float as datetime will throw exception otherwise
        if len(str(end)) == 13:
            end = datetime.fromtimestamp(end / 1000)
        elif len(str(end)) == 10:
            end = datetime.fromtimestamp(end)
        else:
            raise ValueError("End timestamp is outside valid range.")
    else:
        start = start

    # Output timestamps for uniform time series
    timestamps = pd.date_range(start, end, freq=granularity)

    # Create uniform x values for output time series
    x_uniform = np.array([timestamp.timestamp() for timestamp in timestamps])

    # Loop over timeseries (univariate Series or multivariate DataFrame)
    series = []
    for ts in pd.DataFrame(data).columns:
        # extract timeseries as pd.Series and drop NaNs
        observations = pd.DataFrame(data)[ts].dropna()

        # x and y datapoints used to construct linear piecewise function
        x_observed = np.array([index.timestamp() for index in observations.index])
        y_observed = observations.values.squeeze()

        # interpolator function
        interper = scipy.interpolate.interp1d(x_observed, y_observed, kind=kind)

        # If pointwise, sample directly from interpolated (or original) points
        if method == "pointwise":
            y_uniform = interper(x_uniform)
        elif method == "average":
            y_uniform = functional_mean(interper, x_uniform)
        else:
            raise ValueError('Method must be "pointwise" or "average"')

        series.append(pd.Series(data=y_uniform, index=timestamps))

    if isinstance(data, pd.Series):
        return series[0]
    else:
        # dict(zip(.)) recreates original data structure with named columns
        # timestamps as index is already defined by the indivdual Series
        return pd.DataFrame(dict(zip(data.columns, series)))
