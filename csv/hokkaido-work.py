#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#!/usr/bin/env python
# coding: utf-8


# In[ ]:


import codecs
from datetime import datetime as dt
from datetime import timedelta as td
import json
import sys
import numpy as np
import os
import pandas as pd
import plotly
from plotly import subplots
import plotly.express as px
import plotly.tools as tls
import plotly.graph_objects as go
import plotly.io as pio
import plotly.offline as offline
import sys
if "ipy" in sys.argv[0]:
    offline.init_notebook_mode()
from cov19utils import create_basic_plot_figure,     show_and_clear, moving_average,     blank2zero, csv2array,     get_twitter, tweet_with_image,     get_gpr_predict, FONT_NAME, DT_OFFSET,     download_if_needed, json2nparr, code2int, age2int,     get_populations, get_os_idx_of_arr, dump_val_in_arr,     calc_last1w2w_dif, create_basic_scatter_figure,     show_and_save_plotly
import re
import requests


# In[ ]:


def get_gr_name(x):
    if x == 'a':
        return "(アルファ株)"
    if x == 'd':
        return "(デルタ株)"
    if x == 'd+':
        return "(デルタ＋株)"
    return "(変異株)"


# In[ ]:


cats = [
    "飲食店",
    "接待飲食",
    "事業所",
    "福祉施設",
    "医療機関",
    "小学校",
    "中学校",
    "高校",
    "大学",
    "専門学校",
    "警察",
    "自衛隊",
    "教育機関",
    "消防署",
    "運動施設",
    "保育園/幼稚園"]


# In[ ]:





# In[ ]:


def get_template_fig(title, subtitles, today_str):
    figa = subplots.make_subplots(
        shared_xaxes=True,
        rows=4, cols=4, subplot_titles=subtitles,
        horizontal_spacing=0.03, vertical_spacing=0.07)
    figa.update_layout(
        width=800, height=800, template='plotly_dark',
        margin={"r":10,"t":50,"l":10,"b":10},
        title=title + " " + today_str,
        showlegend=False)
    return figa


# In[ ]:


tw_body = "北海道 職域別感染者数 全期間({}～{})".format(start_date, latest_date)
tw_body


# In[ ]:


df = pd.read_csv("maps.csv", encoding='shift-jis', header=0)
latest_date = df['opened'].iloc[-1].replace('/', '-')
start_date = df['opened'].iloc[0].replace('/', '-')
print("start:{} last:{}".format(start_date, latest_date))


# In[ ]:


fig = get_template_fig(tw_body, cats, "")


# In[ ]:


xrange = pd.to_datetime([df['opened'].iloc[0], df['opened'].iloc[-1]], format='%Y/%m/%d')
xrange


# In[ ]:


fig.add_trace(go.Scatter(x=xrange, y=[0, 0], mode='lines', line=dict(width=0, color='red')), 1, 1)


# In[ ]:


cnt = 0
for y in np.arange(4):
    for x in np.arange(4):
        cnt += 1
        sub_df = df[df['id'] == cnt].groupby('opened').sum()
        sub_df['opened'] = sub_df.index.values
        sub_df.index.name = None
        sub_df['opened'] = pd.to_datetime(sub_df['opened'], format='%Y/%m/%d')
        sub_df = sub_df.sort_values('opened')
        trace = go.Scatter(
            x=sub_df['opened'], y=sub_df['patients'], mode='lines+markers',
            marker=dict(color='green', size=3),
            line=dict(width=.5, color='red')
        )
        fig.add_trace(trace, y+1, x+1)


# In[ ]:


fig.update_xaxes(
    range=xrange,
    showgrid=False, showticklabels=False, ticks="", 
    zeroline=True)
fig.update_yaxes(rangemode="tozero")
show_and_save_plotly(fig, "hokkaido-work.jpg", js=False, show=True, image=True, html=True)


# In[ ]:


tw = get_twitter()


# In[ ]:


tweet_with_image(tw, "docs/images/hokkaido-work.jpg", tw_body)


# In[ ]:





# In[ ]:





# In[ ]:




