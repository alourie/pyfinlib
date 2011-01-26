# This is the main lib
# import datetime will need this later on
import numpy as np


def moving_average(x, n, type='simple'):
    """
    Compute an n period moving average.
    x is a simple array.
    type is 'simple' | 'exp' (exp means exponential)
    """

    x = np.asarray(x)
    if type=='exp':
        weights = np.exp(np.linspace(-1., 0., n))
    else:
        weights = np.ones(n)
        
    weights /= weights.sum()
    a = np.convolve(x, weights, mode='full')[:len(x)]
    a[:n] = a[n]
    return a


def macd(x, nslow=26, nfast=12, sig=9):
    """
    Compute the MACD (Moving Average Convergence/Divergence) using a fast and slow exponential moving avg'
    input values are x (array), nslow period and nfast period.
    return values are macd, histogram and signal which are len(x) arrays
    """
    macd = moving_average(x, nfast, type='exponential') - moving_average(x, nslow, type='exponential')
    signal  = moving_average(macd, sig, type='exponential')
    hist = macd - signal
    return macd, hist, signal

def williams_r(x, period=14):
    """
    Compute Williams%R value.
    input values are x (array) and period.
    """
    pass


def relative_strength(prices, n=14):
    """
    compute the n period relative strength indicator
    http://stockcharts.com/school/doku.php?id=chart_school:glossary_r#relativestrengthindex
    http://www.investopedia.com/terms/r/rsi.asp
    """

    deltas = np.diff(prices)
    seed = deltas[:n+1]
    up = seed[seed>=0].sum()/n
    down = -seed[seed<0].sum()/n
    rs = up/down
    rsi = np.zeros_like(prices)
    rsi[:n] = 100. - 100./(1.+rs)

    for i in range(n, len(prices)):
        delta = deltas[i-1] # cause the diff is 1 shorter

        if delta>0:
            upval = delta
            downval = 0.
        else:
            upval = 0.
            downval = -delta

            up = (up*(n-1) + upval)/n
            down = (down*(n-1) + downval)/n

            rs = up/down
            rsi[i] = 100. - 100./(1.+rs)

    return rsi

