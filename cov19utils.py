#!/usr/bin/python3
# coding: utf-8

import chardet
import codecs
from datetime import datetime as dt
from datetime import timedelta as td
import json
import matplotlib.pyplot as plt
import matplotlib.dates as dates
import numpy as np
import os
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
        npa = np.asarray(jsn['data'])
        for l in npa:
            elems = [dt.strptime(l["diagnosed_date"], "%Y-%m-%d")]
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
            if len(elems) > 1:
                delta = dt.strptime(elems.pop(0), "%Y/%m/%d") - from_date
                cnt = 0
                for elem in elems:
                    arr[delta.days][cnt + idx] = blank2zero(elem)
                    cnt += 1
                if k == 'pcr':
                    daily_total = 0
                    for elem in elems:
                        daily_total += blank2zero(elem)
                    arr[delta.days][idx + cnt] = daily_total
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

    print(msg)
    with open(filename, "rb") as imagefile:
        imagedata = imagefile.read()
        params = {"media[]": imagedata, "status": msg}
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


def download_if_needed(base_url, filename):
    """ ファイルが存在しなければダウンロードする """
    if not os.path.exists(filename):
        print("Downloading {} ...".format(filename))
        urlretrieve(base_url + filename, filename)

