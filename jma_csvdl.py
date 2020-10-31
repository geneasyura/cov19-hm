#!/usr/bin/python3
# coding: utf-8
# JMA CSV downloader

import codecs
from datetime import datetime, timedelta, timezone
import lxml.html
import requests

def get_phpsid():
    """ PHP Session ID を取得する """
    r = requests.get("http://www.data.jma.go.jp/gmd/risk/obsdl/index.php")
    tree = lxml.html.fromstring(r.text)
    phpsid = tree.cssselect("input#sid")[0].value
    print("PHP Session ID: {}".format(phpsid))
    return phpsid


def get_jma_payload(city_code):
    """ POST すべきペイロードを生成する """
    yesterday = datetime.now() - timedelta(days=1)
    print(yesterday.year, yesterday.month, yesterday.day)

    return dict(
        stationNumList = '["{}"]'.format(city_code),
        aggrgPeriod = 1,
        # 系列は温湿度固定
        elementNumList = '[["201",""],["605",""],["604",""],["601",""]]',
        interAnnualFlag = 1,
        # COVID-19 感染確認期からのデータと取得する
        ymdList = '["{}","{}","{}","{}","{}","{}"]'.format(
            2020, yesterday.year,
            1, yesterday.month,
            1, yesterday.day),
        optionNumList = '[]',
        downloadFlag = 'true',
        rmkFlag = 1,
        disconnectFlag = 1,
        youbiFlag = 0,
        fukenFlag = 1,
        kijiFlag = 0,
        huukouFlag = 0,
        csvFlag = 1,
        jikantaiFlag = 0,
        jikantaiList = '[]',
        ymdLiteral = 1,
        PHPSESSID = get_phpsid()
    )


def get_jma_headers():
    """ POST用HTTPヘッダを生成する """
    ua = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'
    return {
        'User-Agent': ua,
        'Accept-Language': 'ja,en-US;q=0.9,en;q=0.8',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Referer': 'http://www.data.jma.go.jp/gmd/risk/obsdl/index.php'
    }


def save_jma_data(filename, city_code="s47412"):
    """ JMA からCSVデータをダウンロードし、ファイルに保存する """
    url = "http://www.data.jma.go.jp/gmd/risk/obsdl/show/table"
    r = requests.post(url, data=get_jma_payload(city_code), headers=get_jma_headers())
    print(r.status_code)
    f=codecs.open(filename, "wb")
    f.write(r.content)
    f.close()
    print("Wrote {} bytes into {}".format(len(r.content), filename))


def parse_jma_csv(filename):
    """ JMAのCSVデータを解析し、リスト型で格納する """
    weather_info = []
    with codecs.open(filename, encoding="shift-jis") as f:
        for i in range(6):
            l = f.readline() # 6行スキップ
        while l:
            l = f.readline().replace("\r\n", "")
            arr = l.split(',')
            if len(arr) == 13:
                ts = datetime.strptime(arr[0], "%Y/%m/%d")
                temp = float(arr[ 1])
                rh = float(arr[ 4])
                vp = float(arr[ 7])
                ap = float(arr[10])
                ah = 18.0 * ((100.0 * vp) / (8.31447 * (273.15 + temp)))
                weather_info.append([
                    ts,
                    temp,  # 平均気温[℃]
                    rh,    # 平均湿度[%RH]
                    vp,    # 平均蒸気圧 [hPa]
                    ap,    # 平均現地気圧
                    ah     # 容積絶対湿度 [g/㎥]
                ])
        pass
    return weather_info







