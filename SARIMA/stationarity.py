# stationarity.py
from statsmodels.tsa.stattools import adfuller


def adf_test(series):
    """
    Perform the Augmented Dickey-Fuller test to check for stationarity.
    Args:
        series (pd.Series): The time series data to test.
    Returns:
        bool: Whether the series is stationary (p-value < 0.05).
    """
    result = adfuller(series)
    print(f"ADF Statistic: {result[0]}")
    print(f"p-value: {result[1]}")
    if result[1] > 0.05:
        print("Series is non-stationary. Differencing will be applied.")
        return False
    else:
        print("Series is stationary.")
        return True


def apply_differencing(series, order=1):
    """
    Apply differencing to make the series stationary.
    Args:
        series (pd.Series): The time series data.
        order (int): The order of differencing.
    Returns:
        pd.Series: The differenced series.
    """
    return series.diff(periods=order).dropna()
