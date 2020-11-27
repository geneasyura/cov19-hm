#!/usr/bin/python3
# coding: utf-8

import chardet
import codecs
from datetime import datetime as dt
from datetime import timedelta as td
from japanmap import picture
import json
import matplotlib.pyplot as plt
import matplotlib.dates as dates
import matplotlib.cm as cm
import numpy as np
import os
import pandas as pd
from PIL import Image
import plotly
import plotly.express as px
import plotly.tools as tls
import plotly.graph_objects as go
import plotly.io as pio
import plotly.offline as offline
from scipy.optimize import curve_fit
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import WhiteKernel, ExpSineSquared, RBF, ConstantKernel
import sys
from twitter import Twitter, OAuth
from urllib.request import urlretrieve
import yaml

# フォント名
FONT_NAME = 'MS Gothic'
# 統計開始日時
DT_OFFSET = "2020/1/16"


def json2nparr(keys, filename):
    """ JSON データを nparray に加工 """
    lst = []
    with codecs.open(filename, encoding='utf-8') as f:
        jsn = json.load(f)
        print("{} 更新日: {}".format(filename, jsn['date']))
        if "patient" not in filename:
            npa = np.asarray(jsn['data'])
        else:
            npa = np.asarray(jsn['datasets']['data'])
        for l in npa:
            if "patient" not in filename:
                elems = [dt.strptime(l["diagnosed_date"], "%Y-%m-%d")]
            else:
                elems = [0]
            for k in keys:
                if l[k] is None:
                    elems.append(0)
                else:
                    elems.append(l[k])
            lst.append(elems)
    return np.array(lst)


def create_basic_plot_figure():
    """ 基本グラフを作成する """
    plt.style.use("dark_background")
    fig, ax = plt.subplots(figsize=(20,10))
    ax.xaxis.set_major_locator(dates.DayLocator(bymonthday=None, interval=7, tz=None))
    ax.xaxis.set_major_formatter(dates.DateFormatter("%Y-%m-%d"))
    plt.ylabel('人数', fontname=FONT_NAME)
    plt.grid(True)
    plt.xticks(rotation=90, fontsize=10)
    return fig, ax



def show_and_clear(fig, filename):
    """ グラフを表示またはファイルに保存する """
    if "ipy" in sys.argv[0]:
        plt.show()
    fig.savefig(filename)
    #fig.savefig(filename.replace(".jpg", ".svg"), format="svg", dpi=120)
    fig.clear()


def moving_average(data, periods=7):
    """ 移動平均を算出する """
    w = np.ones(periods) / periods
    ret = np.convolve(data, w, mode='valid')
    ret = np.insert(ret, 0, [0 for i in range(periods - 1)])
    return ret


def blank2zero(code):
    """ 空文字を0に変換する """
    if len(code) == 0:
        return 0
    try:
        ret = int(code)
    except:
        ret = float(code)
    return ret


def code2int(code):
    """ 空文字を不定-1に変換する """
    if len(code) == 0:
        return -1
    return int(code)


def age2int(age):
    """ 年齢を整数に変換する """
    x = age.replace('-', '-1').replace('代', '').replace('10歳未満', '0').replace('100歳以上', '100').replace('不明', '-1')
    if len(x) == 0:
        return -1
    return int(x)


def csv2array(arr, k, filename, idx, dt_os=DT_OFFSET):
    """ CSVをnp arrayに変換する """
    from_date = dt.strptime(dt_os, "%Y/%m/%d")
    
    default_enc = "shift-jis"
    with open(filename, "rb") as f:
        enc = chardet.detect(f.readline())
        print("file: {} enc: {}".format(filename, enc['encoding']))
        if enc['encoding'] is not None:
            default_enc = enc['encoding']
    
    with codecs.open(filename, encoding=default_enc) as f:
        l = f.readline()
        while l:
            l = f.readline().replace("\r\n", "")
            elems = l.split(',')
            if len(elems) > 1 and len(elems[0]) > 0:
                delta = dt.strptime(elems.pop(0), "%Y/%m/%d") - from_date
                cnt = 0
                for elem in elems:
                    arr[int(delta.days)][cnt + idx] = blank2zero(elem)
                    cnt += 1
                    if k == 'pcr' and cnt == 6: break
                if k == 'pcr':
                    daily_total = 0
                    for elem in elems:
                        daily_total += blank2zero(elem)
                    #print("delta:{} idx:{} cnt:{} total:{}.".format(delta.days, idx, cnt, daily_total))
                    arr[int(delta.days)][idx + cnt] = daily_total
    pass


def get_twitter():
    """ Twitterインスタンスを取得する """
    tw_cfg = yaml.load(open(".tokens"), Loader=yaml.SafeLoader)
    tw = Twitter(auth=OAuth(
        tw_cfg['ACCESS_TOKEN'], tw_cfg['ACCESS_TOKEN_SECRET'],
        tw_cfg['CONSUMER_KEY'], tw_cfg['CONSUMER_SECRET']))
    return tw


def tweet_with_image(twtr, filename, msg):
    """ tweet する """
    if "ipy" in sys.argv[0]:
        return

    #return

    #print(msg)
    with open(filename, "rb") as imagefile:
        imagedata = imagefile.read()
        params = {"media[]": imagedata, "status": msg + " #COVID19"}
        req = twtr.statuses.update_with_media(**params)
        print(req['created_at'])
    print("Tweeted.")


def get_gpr_predict(x, y, x_pred, rbf=80, c=10, w=200):
    """ ガウス過程回帰の予測系列を取得する """
    gp_kernel = RBF(rbf) + ConstantKernel(c) + WhiteKernel(w)
    gpr = GaussianProcessRegressor(
        kernel=gp_kernel,
        alpha=1e-1, 
        optimizer="fmin_l_bfgs_b",
        n_restarts_optimizer=10,
        normalize_y=True)
    offset = -1
    for i in np.arange(len(y)):
        if y[-i-1] > 0:
            offset = -i-1
            print("y {} val = {}.".format(i, y[-i-1]))
            break
    if offset != -1:
        print("data {} offset = {}.".format(len(y), offset))
        gpr.fit(x[:offset], y[:offset])
    else:
        gpr.fit(x, y)
    y_pred = gpr.predict(x_pred, return_std=False)
    return y_pred


def download_if_needed(base_url, filename, savename=None):
    """ ファイルが存在しなければダウンロードする """
    if savename is None:
        savename = filename
    if not os.path.exists(savename):
        print("Downloading {} ...".format(filename))
        urlretrieve(base_url + filename, savename)
        print("Saved as {}.".format(savename))


def get_populations():
    """ 都道府県の人口情報を取得する """
    populations = {}
    all_population = 0
    with codecs.open("population.txt", encoding='utf-8') as f:
        l = f.readline()
        while l:
            elems = l.split(',')
            populations[elems[3]] = dict(
                region = int(elems[0]), 
                code   = int(elems[1]),
                ja     = elems[2],
                en     = elems[3],
                total = int(elems[4])
            )
            all_population += int(elems[4])
            l = f.readline().replace("\r\n", "").rstrip()
    print("All population in Japan: {}".format(all_population))
    return populations


def get_os_idx_of_arr(arr, delta_days):
    """ データ最終更新日Indexを取得する """
    os_idx = -1
    for i in np.arange(delta_days):
        if np.sum(arr[-i -1, 1:])  > 0:
            os_idx = -i -1
            print("Data offset index: {}".format(os_idx))
            break
    return os_idx


def dump_val_in_arr(populations, arr, prefix, dec_num=1):
    """ 各都道府県の数値を表示する """
    print("{}: ".format(prefix), end="")
    for k, v in populations.items():
        strfmt = "{}={:." + str(dec_num) + "f} "
        print(strfmt.format(v['ja'], np.round(arr[v['code']], dec_num)), end="")
    print("")


def calc_last1w2w_dif(arr, delta_days):
    """ 直近１、2週間差分を取得する """
    idx = get_os_idx_of_arr(arr, delta_days)
    latest_arr = arr[idx] # 最新
    last1w_arr = arr[idx -  7] # 1週間前
    last2w_arr = arr[idx - 14] # 2週間前
    diff1w_arr = latest_arr - last1w_arr # 最新と1週間前の差分
    diff2w_arr = latest_arr - last2w_arr # 最新と2週間前の差分
    return diff1w_arr, diff2w_arr


def create_basic_scatter_figure(xlabel, ylabel):
    """ 基本散布図テンプレートを作成する """
    plt.close()
    plt.style.use("dark_background")
    fig = plt.figure(figsize=(9, 9))
    ax = fig.add_subplot(111)
    plt.xlabel(xlabel, fontname=FONT_NAME)
    plt.ylabel(ylabel, fontname=FONT_NAME)
    plt.grid(True)
    #plt.subplots_adjust(left=0.07, right=0.97, bottom=0.07, top=0.97)
    return fig, ax


def make_japan_heatmap(filename, title, npa1d, populations):
    """ 都道府県別ヒートマップを表示する """
    fig = go.Figure()
    w = 610
    h = 630
    cmap = plt.get_cmap("plasma")
    norm = plt.Normalize(vmin=np.min(npa1d[1:]), vmax=np.max(npa1d[1:]))
    fcol = lambda x: '#' + bytes(cmap(norm(x), bytes=True)[:3]).hex()
    fig.add_trace(go.Scatter(x=[0, w], y=[0, h], mode='markers', marker_opacity=0))
    fig.add_trace(go.Heatmap(x=[0, 0], y=[0, 0], opacity=0,
        z=[np.min(npa1d[1:]), np.max(npa1d[1:])],
        zmin=np.min(npa1d[1:]), zmax=np.max(npa1d[1:]),
        type='heatmap', colorscale='plasma', showscale=True))
    map_cols = {}
    for k, v in populations.items():
        map_cols[v['ja']] = fcol(npa1d[v['code']])
    pict = picture(map_cols)
    axis_template = lambda x: dict(
        range=[0, x], autorange=False, showgrid=False, zeroline=False,
        linecolor='black', showticklabels=False, ticks='')
    fig.update_layout(title=title, xaxis=axis_template(w), yaxis=axis_template(h),
                     showlegend=False, width=w, height=h, autosize=False,
                      margin={"l": 0, "r": 0, "t":40, "b": 0}
                     )
    fig.add_layout_image(dict(
            x=0, sizex=w, y=h, sizey=h, xref="x", yref="y", opacity=1,
            layer="below", sizing="stretch", source=Image.fromarray(pict)))
    show_and_save_plotly(fig, filename, js=False, show=True, image=True, html=False)


def make_japan_choropleth(filename, title, npa1d):
    """ 日本の choropleth を作成する """
    f = codecs.open("japan-min.geojson", "r", encoding='utf-8')
    geojson = json.load(f)
    f.close()
    df = pd.read_csv('population.txt',
                     header=None, names=['reg', 'code', 'name', 'en', 'total', 'color'],
                     dtype={'reg':int, 'code':int, 'name':str, 'total':int, 'color':float})
    for i in range(len(npa1d)):
        df.loc[i, 'color'] = npa1d[i]
        #print(i, df.loc[i, 'color'], df.loc[i, 'name'], npa1d[i])
        i += 1
    fig = px.choropleth(df, geojson=geojson, color="color", hover_name='name',
                    locations="code", featureidkey="properties.id",
                    labels={'color':'値', 'code':'都道府県コード'},
                    projection="mercator", title=title)
    fig.update_geos(visible=False,
                    lonaxis=dict(range=[127.632493, 145.792893]),
                    lataxis=dict(range=[26.089333, 45.531737]))
    fig.update_layout(margin={"r":0,"t":40,"l":0,"b":0})
    show_and_save_plotly(fig, filename, js=False, show=False, image=False, html=True)


def show_and_save_plotly(fig, filename, js='directory', show=True, image=True, html=True):
    """ plotly graph をファイルに保存する """
    fig.update_layout(template='plotly_dark')
    if "ipy" in sys.argv[0] and show:
        offline.iplot(fig)
    if image:
        jpgname = 'docs/images/{}'.format(filename)
        pio.write_image(
            fig, file=jpgname,
            format='jpeg', engine="kaleido")
        print("wrote to {}".format(jpgname))
    if html:
        htmlname = 'docs/_includes/{}'.format(filename.replace("jpg", "html"))
        pio.write_html(
            fig, file=htmlname,
            include_plotlyjs=js, auto_play=False, full_html=False)
        print("wrote to {}".format(htmlname))
    pass


def make_exp_fit_graph(twt, xbins, ybins, title, imgname, htmlname, linkhtml, needs_tw=True):
    """ 倍加時間近似関数をプロットする """
    xdays = np.array([i.days for i in (xbins - xbins[0])])
    xrange = np.arange(len(xdays))
    (a, b, c), p0 = curve_fit(
        lambda t, a, b, c: a * 2 ** (b * t) + c, xrange, ybins, 
        p0=[1, 1, 1], maxfev=1000)
    print(a, b, c)
    pred_days = 14
    xrange = np.arange(pred_days + len(xdays))
    y_fit = np.array([a * 2 ** (b * i) + c for i in xrange])
    x_pred = np.array(xbins)
    for i in np.arange(pred_days):
        x_pred = np.append(x_pred, (xbins[-1] + td(days=int(1 + i))))
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=xbins, y=ybins, mode='markers', name='新規感染者',
        marker=dict(size=4)))
    fig.add_trace(go.Scatter(
        x=x_pred, y=y_fit, name="$a2^{bx}+c$",
        line=dict(width=1)))
    fig.update_layout(
        xaxis=dict(title='日付', type='date', 
                   dtick=604800000.0, tickformat="%_m/%-d"),
        yaxis=dict(title='人数', type='log'),
        title=title)
    show_and_save_plotly(
        fig, imgname, js=False, show=True, image=True, html=True)
    ab_params = " (a=%.2f, b=%.2f, c=%.2f) " % (a, b, c)
    tw_body = title + ab_params
    if b > 0.0:
        doubling_time = " 倍加時間:%.2f 日 " % (1.0 / b)
        print(doubling_time)
        tw_body += doubling_time
        htm_name = "docs/_includes/{}".format(htmlname)
        with codecs.open(htm_name, "w", encoding='utf-8') as f:
            f.write("<div>{} {}</div>".format(doubling_time, ab_params))
    else:
        print("Error: failed to fit.")
    tw_body += " https://geneasyura.github.io/cov19-hm/{} ".format(linkhtml)
    tweet_with_image(twt, "docs/images/{}".format(imgname), tw_body)

