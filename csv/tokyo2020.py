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


df = pd.read_csv('tokyo2020.csv')


# In[ ]:


1209600000/16


# In[ ]:


fig = go.Figure()
fig.add_trace(go.Bar(opacity=0.6,x=df['date'], y=df['cases'], name='Olympic'))
fig.add_trace(go.Bar(opacity=0.6,x=df['date'], y=df['para'],  name='Paralympic'))
fig.update_layout(
    title='Daily new confirmed COVID-19 positive cases in Tokyo-2020',
    template='plotly_dark', xaxis_title='date', yaxis_title='new cases',
)
fig.update_layout(
    width=800, height=600,
    xaxis=dict(title='date', type='date',
               dtick=75600000.0, tickformat="%_m/%-d",
              ),
    margin={"r":20,"t":80,"l":20,"b":80},
    barmode='stack'
)
show_and_save_plotly(
    fig, "tokyo2020.jpg", js=False, show=True, image=True, html=False)


# In[ ]:





# In[ ]:




