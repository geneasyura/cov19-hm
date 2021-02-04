#!/usr/bin/python3
# coding: utf-8

import numpy as np
import plotly.graph_objects as go
from scipy import fftpack

def fft_denoise(x, y, showFigure=True, freq_int=0.15, freq_th=0.18, freq_min_A=0.03):
    n = len(x)

    if showFigure:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=y))
        fig.show()

    y_hat = fftpack.fft(y) / (n/2)

    if showFigure:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=y_hat.real))
        fig.show()

    freq = fftpack.fftfreq(n, freq_int)

    if showFigure and False:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=freq))
        fig.show()

    y_hat[freq < 0] = 0
    y_hat[freq > freq_th] = 0
    y_hat[np.abs(y_hat) < freq_min_A] = 0

    if showFigure:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=y_hat.real))
        fig.show()

    y2 = np.real(fftpack.ifft(y_hat) * (n))

    if showFigure:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=y, mode='lines',
            line=dict(width=.5, color='red')))
        fig.add_trace(go.Scatter(x=x, y=y2, mode='lines+markers',
            marker=dict(size=1, color='blue')))
        fig.show()

    return y2
