#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#!/usr/bin/env python
# coding: utf-8


# In[ ]:


import codecs
from datetime import datetime as dt
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


import tabula


# In[ ]:


dfs = tabula.read_pdf("000816269.pdf", lattice=True, pages='33-34')
#display(dfs)


# In[ ]:


dfs[0].columns = ["Lot", "Start", "Total", "React", "Serious", "Death", "Anaphylaxis"]
df0 = dfs[0].dropna()
dfs[1].columns = ["Lot", "Start", "Total", "React", "Serious", "Death", "Anaphylaxis"]
df1 = dfs[1].dropna()


# In[ ]:


df2 = (pd.concat([df0, df1]))


# In[ ]:


df2


# In[ ]:


def isfloat(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


# In[ ]:


def s2f(s):
    tmp = str(s).replace(',', '')
    if tmp.isdigit():
        return int(tmp)
    if isfloat(tmp):
        return float(tmp)
    if "令和" in tmp:
        tmp = tmp.replace("令和3", "2021")
    return tmp


# In[ ]:





# In[ ]:


df2.columns = ["Lot", "Start", "Total", "React", "Serious", "Death", "Anaphylaxis"]
total = df2[df2["Start"] == '-']
total = total[total['Lot'] != '不明']


# In[ ]:


df2 = df2.applymap(s2f)
df2 = df2[df2['Lot'] != '不明']
df2 = df2[df2['Start'] != '-' ]
df2['Start'] = pd.to_datetime(df2['Start'], format='%Y年%m月%d日')


# In[ ]:


total = total.applymap(s2f)
total


# In[ ]:


df2


# In[ ]:


df2["r_React"] = 100.0 * (df2["React"] / df2["Total"])
df2["r_Serious"] = 100.0 * (df2["Serious"] / df2["Total"])
df2["r_Death"] = 100.0 * (df2["Death"] / df2["Total"])
df2["r_Anaphylaxis"] = 100.0 * (df2["Anaphylaxis"] / df2["Total"])


# In[ ]:


total["r_React"] = (total["React"] / total["Total"]) * 100.0
total["r_Serious"] = (total["Serious"] / total["Total"]) * 100.0
total["r_Death"] = (total["Death"] / total["Total"]) * 100.0
total["r_Anaphylaxis"] = (total["Anaphylaxis"] / total["Total"]) * 100.0


# In[ ]:


total['Lot'] = "Total"
total


# In[ ]:


df2['d_React']       = df2['r_React'] / total['r_React'].values[0]
df2['d_Serious']     = df2['r_Serious'] / total['r_Serious'].values[0]
df2['d_Death']       = df2['r_Death'] / total['r_Death'].values[0]
df2['d_Anaphylaxis'] = df2['r_Anaphylaxis'] / total['r_Anaphylaxis'].values[0]


# In[ ]:


df2


# In[ ]:


fig = subplots.make_subplots(specs=[[{"secondary_y": True}]])
fig.add_trace(go.Bar(opacity=0.6,
    x=df2['Lot'], y=df2['Total'], name='推定接種数',), secondary_y=False)
fig.add_trace(go.Scatter(
    x=df2['Lot'], y=df2['r_Serious'], name = '重篤率',
    mode='lines+markers', line=dict(width=2)), secondary_y=True)
fig.add_trace(go.Scatter(
    x=df2['Lot'], y=df2['r_Death'], name='死亡率',
    mode='lines+markers', line=dict(width=2)), secondary_y=True)
fig.add_trace(go.Scatter(
    x=df2['Lot'], y=df2['r_Anaphylaxis'], name='アナフィラキシー率',
    mode='lines+markers', line=dict(width=2)), secondary_y=True)
fig.update_layout(
    title='2021/8/4 コミナティ筋注(ファイザー) ロット別報告件数',
    template='plotly_dark', xaxis_title='ロット [Lot]',
    yaxis_title='推定接種回数 (人数ではない)',
    yaxis2_title='報告割合 [%] (人数ではない)',
)
fig.update_layout(
    width=950,
    yaxis=dict(range=[0, np.max(df2['Total']) * 1.08]),
    yaxis2=dict(range=[0, np.max(df2['r_Anaphylaxis']) * 1.08]))
show_and_save_plotly(fig, "000816269.jpg", js=False, show=True, image=True, html=True)


# In[ ]:





# In[ ]:


fig = subplots.make_subplots(specs=[[{"secondary_y": True}]])
fig.add_trace(go.Bar(opacity=0.6,
    x=df2['Lot'], y=df2['Total'], name='推定接種数',), secondary_y=False)
fig.add_trace(go.Scatter(
    x=df2['Lot'], y=df2['d_Serious'], name = '重篤率',
    mode='lines+markers', line=dict(width=2)), secondary_y=True)
fig.add_trace(go.Scatter(
    x=df2['Lot'], y=df2['d_Death'], name='死亡率',
    mode='lines+markers', line=dict(width=2)), secondary_y=True)
fig.add_trace(go.Scatter(
    x=df2['Lot'], y=df2['d_Anaphylaxis'], name='アナフィラキシー率',
    mode='lines+markers', line=dict(width=2)), secondary_y=True)
fig.update_layout(
    title='2021/8/4 コミナティ筋注(ファイザー) ロット別報告件数 [全体平均比]',
    template='plotly_dark', xaxis_title='ロット [Lot]',
    yaxis_title='推定接種回数 (人数ではない)',
    yaxis2_title='全体平均に対する報告割合 [%] (人数ではない)',
)
fig.update_layout(
    width=950,
    yaxis=dict(range=[0, np.max(df2['Total']) * 1.08]),
    yaxis2=dict(range=[0, np.max(df2['d_Anaphylaxis']) * 1.08]))
show_and_save_plotly(fig, "000816269-2.jpg", js=False, show=True, image=True, html=True)


# In[ ]:





# In[ ]:


df_all = (pd.concat([df2, total]))
df_all.to_csv("000816269.csv")


# In[ ]:




