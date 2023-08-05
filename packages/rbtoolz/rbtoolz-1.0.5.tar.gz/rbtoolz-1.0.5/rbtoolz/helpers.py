#!/usr/bin/env python
# -*- coding: utf-8 -*-


""" Helper functions primarily for data analysis

"""


__author__ = 'Ross Bonallo'
__license__ = 'MIT Licence'
__version__ = '1.0.3'


import pandas as pd
import numpy as np

def seag(df,period='M',agg='sum'):

    if agg == 'mean':
        agg_func = np.mean
    else:
        agg_func = np.sum

    if period == 'M':
        _df = pd.pivot_table(df,index=df.index.day,columns=df.index.month,
                aggfunc=agg_func,fill_value=0)
    elif period == 'W':
        _df = pd.pivot_table(df,index=df.index.dayofweek,columns=df.index.year,
                aggfunc=agg_func,fill_value=0)
    elif period == 'WA':
        _df = pd.pivot_table(df,index=df.index.week,columns=df.index.year,
                aggfunc=agg_func,fill_value=0)
    elif period == 'Y':
        _df = pd.pivot_table(df,index=df.index.dayofyear,columns=df.index.year,
                aggfunc=agg_func,fill_value=0)
    else:
        raise Exception('Period {} not available'.format(period))
    return _df
