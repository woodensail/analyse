# -*- coding: utf-8 -*-
__author__ = 'sail'
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pylab import *
import sqlite3
import common
from datetime import datetime
from dateutil.parser import parse

from datetime import datetime, date, time

# collaborative, interactive, publication-quality graphs.
import plotly.plotly as py
from plotly.graph_objs import *

def s104(usrid=None, name=None):
    if not usrid:
        usrid=common.get_id(name)
    conn = sqlite3.connect(r'resource/chat.db')
    df =pd.read_sql('SELECT * FROM chatdb WHERE usrid =?',conn,params=(usrid,),parse_dates=['date'],index_col=['date'])
    # print(df[['usrid','name'],['name']].groupby(df.usrid).count().head(5))
    df.insert(0,'count',df['id'])
    df.groupby(lambda x:x.dayofweek).count()[['count']].plot(kind='bar')
    df[['count']].resample("M", how="count").plot();
    df2 =pd.read_sql('SELECT * FROM chatdb WHERE usrid =?',conn,params=(usrid,),parse_dates=['time'],index_col=['time'])
    print(df2)
    df2.insert(0,'count',df2['id'])
    df2.groupby(lambda x:x.hour).count()[['count']].plot(kind='bar')
    # df['count'].resample("M", how="count").plot(lw=2);
    # df[['count']].groupby(df.date).count().plot(kind='bar')
    plt.show()

def tttt(t):

    print(parse(t,dayfirst=True))
