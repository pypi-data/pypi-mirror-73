import math
import logging
import time

# Util functions
def get_current_timestamp():
    """Function that gets timestamp

    Returns:
        int -- timestamp in milliseconds. if None, there is a problem with the connection.
    """
    timestamp = int(time.time() * 1000)
    return timestamp

def calculate_share(equity, risk_factor, current_atr, custom_position_risk):
    """Calculates the number of shares to buy or sell according to given parameters

    Arguments:
        equity {float} -- amount of equity
        risk_factor {float} -- risk factor
        current_atr {float} -- current atr
        custom_position_risk {float} -- custom position risk

    Returns:
        float -- number of shares to buy or sell
    """
    risk = equity * custom_position_risk
    share = risk / (risk_factor * current_atr)
    return round(share, 6)

def truncate_floor(number, decimals):
    """Truncates decimals to floor based on given parameter

    Arguments:
        number {float} -- number to truncate
        decimals {int} -- number of decimals

    Returns:
        float -- truncated number
    """
    return math.floor(number * 10 ** decimals) / 10 ** decimals

def truncate_ceil(number, decimals):
    """Truncates decimals based on given parameter

    Arguments:
        number {float} -- number to truncate
        decimals {int} -- number of decimals

    Returns:
        float -- truncated number
    """
    return math.ceil(number * 10 ** decimals) / 10 ** decimals