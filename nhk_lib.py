#!/usr/bin/env python
# coding: utf-8
from cov19utils import moving_average
from datetime import datetime as dt
import numpy as np
import os
import pandas as pd
from plotly import subplots
import plotly.graph_objects as go
import requests
import sys

class ColumnNames:
    def __init__(self):
        self.ts         = '日付'
        self.pref_code  = '都道府県コード'
        self.pref_name  = '都道府県名'
        self.case       = '各地の感染者数_1日ごとの発表数'
        self.total_case = '各地の感染者数_累計'
        self.death      = '各地の死者数_1日ごとの発表数'
        self.total_death='各地の死者数_累計'
        pass


def get_nhk_df(filename):
    uri = "https://www3.nhk.or.jp/n-data/opendata/coronavirus/"
    name = "nhk_news_covid19_prefectures_daily_data.csv"
    referer = "https://www3.nhk.or.jp/news/special/coronavirus/data-widget/"
    ua = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5)"
    ua += " AppleWebKit/537.36 (KHTML, like Gecko)"
    ua += " Chrome/67.0.3396.99 Safari/537.36"
    headers = {'User-Agent': ua, 'referer': referer}

    if not os.path.exists(filename):
        print("Downloading {}...".format(name))
        response = requests.get(uri + name, headers=headers)
        f = open(filename, "w")
        lines = response.text.split("\n")
        for line in lines:
            l = line.strip()
            if len(l) > 0:
                f.write(l + "\n")
        f.close()

    df = pd.read_csv(filename, encoding='shift-jis', header=0)
    return df

def get_nhk_keys():
    return ColumnNames()

def get_lr_col(v):
    c = 'green'
    if v < -0.5:
        c = 'blue'
    if v >= -0.5:
        c = 'royalblue'
    if v > 0.2:
        c = 'orange'   
    if v > 0.5:
        c = 'red'
    if v < 0.2 and v > -0.2:
        c = 'green'
    return c

def add_pref2fig(df, lr, i, x, y, X, fig, prefs):
    k = ColumnNames()
    dfh = df[ df['都道府県名'] == prefs[i]]
    df14 = dfh[-14:]
    Y = df14[k.case].values
    lr.fit(X.reshape(-1, 1), Y.reshape(-1, 1))
    Y_pred = lr.predict(X.reshape(-1, 1)).reshape(1, -1)[0]
    a = lr.coef_[0][0]
    lr_col = get_lr_col(a)
    trace_xy = go.Scatter(
        x=X, y=Y, mode='lines',
        line=dict(width=2, color='white'))
    trace_lr = go.Scatter(
        x=X, y=Y_pred, mode='lines',
        line=dict(width=2, color=lr_col))
    fig.add_trace(trace_xy, y, x)
    fig.add_trace(trace_lr, y, x)

def update_axes(fig):
    fig.update_xaxes(
        showgrid=False, showticklabels=False, ticks="",
        zeroline=False)
    fig.update_yaxes(
        showgrid=False, showticklabels=False, ticks="",
        zeroline=False)

def update_layout(fig, title, today_str):
    fig.update_layout(
        margin={"r":5,"t":50,"l":5,"b":5},
        width=600, height=400, template='plotly_dark',
        title=title + " " + today_str, showlegend=False)


def get_template_fig(prefs):
    figa = subplots.make_subplots(
        rows=4, cols=6, subplot_titles=prefs[:24],
        horizontal_spacing=0.03, vertical_spacing=0.07)
    figb = subplots.make_subplots(
        rows=4, cols=6, subplot_titles=prefs[24:],
        horizontal_spacing=0.03, vertical_spacing=0.07)
    return figa, figb
