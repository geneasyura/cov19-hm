#!/usr/bin/python3
# coding: utf-8
# This source code is based on japanmap: https://github.com/SaitoTsutomu/japanmap

import codecs
from cv2 import imread, cvtColor, COLOR_BGR2RGB
import matplotlib.pyplot as plt
import matplotlib.dates as dates
import matplotlib.cm as cm
import numpy as np
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
from pathlib import Path

FONT_NAME = 'MS Gothic'

# 振興局情報
sub_prefs = {
     # （2020年7月31日 住民基本台帳）
     0: dict(name="非公表"    , code="00", suffix="その他",     total=9999999),
     1: dict(name="石狩"      , code="01", suffix="振興局"    , total=2385306),
     2: dict(name="渡島"      , code="02", suffix="総合振興局", total= 385954),
     3: dict(name="檜山"      , code="03", suffix="振興局"    , total=  34589),
     4: dict(name="後志"      , code="04", suffix="総合振興局", total= 202399),
     5: dict(name="空知"      , code="05", suffix="総合振興局", total= 284613),
     6: dict(name="上川"      , code="06", suffix="総合振興局", total= 486430),
     7: dict(name="留萌"      , code="07", suffix="振興局"    , total=  44066),
     8: dict(name="宗谷"      , code="08", suffix="総合振興局", total=  62000),
     9: dict(name="オホーツク", code="09", suffix="総合振興局", total= 274757),
     10:dict(name="胆振"      , code="10", suffix="総合振興局", total= 384448),
     11:dict(name="日高"      , code="11", suffix="振興局"    , total=  64725),
     12:dict(name="十勝"      , code="12", suffix="総合振興局", total= 335432),
     13:dict(name="釧路"      , code="13", suffix="総合振興局", total= 225158),
     14:dict(name="根室"      , code="14", suffix="振興局"    , total=  73102)
}


# 振興局内の市町村
city_towns = {
    0: "非公表 中国".split(),
    1: "札幌市 江別市 千歳市 恵庭市 北広島市 石狩市 当別町 新篠津村".split(),
    2: "函館市 松前町 福島町 知内町 木古内町 北斗市 七飯町 鹿部町 森町 八雲町 長万部町".split(),
    3: "江差町 上ノ国町 厚沢部町 乙部町 せたな町 今金町 奥尻町".split(),
    4: "小樽市 島牧村 寿都町 黒松内町 蘭越町 ニセコ町 真狩村 留寿都村 喜茂別町 京極町 倶知安町 共和町 岩内町 泊村 神恵内村 積丹町 古平町 仁木町 余市町 赤井川村".split(),
    5: "夕張市 岩見沢市 美唄市 芦別市 赤平市 三笠市 滝川市 砂川市 歌志内市 深川市 南幌町 奈井江町 上砂川町 由仁町 長沼町 栗山町 月形町 浦臼町 新十津川町 妹背牛町 秩父別町 雨竜町 北竜町 沼田町 幌加内町".split(),
    6: "旭川市 士別市 名寄市 富良野市 鷹栖町 東神楽町 当麻町 比布町 愛別町 上川町 東川町 美瑛町 和寒町 剣淵町 下川町 上富良野町 中富良野町 南富良野町 占冠村 美深町 音威子府村 中川町".split(),
    7: "留萌市 増毛町 小平町 苫前町 羽幌町 初山別村 遠別町 天塩町 幌延町".split(),
    8: "稚内市 猿払村 浜頓別町 中頓別町 枝幸町 豊富町 礼文町 利尻町 利尻富士町".split(),
    9: "北見市 網走市 紋別市 大空町 美幌町 津別町 斜里町 清里町 小清水町 訓子府町 置戸町 佐呂間町 遠軽町 湧別町 滝上町 興部町 西興部村 雄武町".split(),
    10:"室蘭市 苫小牧市 登別市 伊達市 豊浦町 洞爺湖町 壮瞥町 白老町 安平町 厚真町 むかわ町".split(),
    11:"日高町 平取町 新冠町 新ひだか町 浦河町 様似町 えりも町".split(),
    12:"帯広市 新得町 清水町 幕別町 池田町 豊頃町 本別町 音更町 士幌町 上士幌町 鹿追町 芽室町 中札内村 更別村 大樹町 広尾町 足寄町 陸別町 浦幌町".split(),
    13:"釧路市 釧路町 厚岸町 浜中町 標茶町 弟子屈町 鶴居村 白糠町".split(),
    14:"根室市 別海町 中標津町 標津町 羅臼町 色丹村 泊村 留夜別村 留別村 紗那村 蘂取村".split(), # 後志の泊村と重複する
}


def get_sub_code(name):
    """ 振興局コードを取得する """
    for k, v in sub_prefs.items():
        if v['name'] != "" and name.startswith(v['name']):
            return k

    for k, v in city_towns.items():
        if len(v) > 0 and name in v:
            return k

    return 0


def get_svg_txt(dic=None, rate=1):
    """ SVG のテキストを取得する """
    f = codecs.open(str(Path(__file__).parent / "Subprefectures_of_Hokkaido.svg"), encoding="utf-8")
    p = f.read()
    if hasattr(dic, "items"):
        for k, v in dic.items():
            i = k if isinstance(k, int) else int(k.lstrp("0"))
            if 0 <= i <= 14:
                p = p.replace("#c%02d" % (k), v)
    return p


def get_hokkaido(dic=None, ret=1):
    """ 塗り分け済み Hokkaido の nparray 画像情報を取得する """
    txt = get_svg_txt(dic, ret)
    filename = str(Path(__file__).parent / "svglib.tmp")
    f = codecs.open(filename, "w", encoding="utf-8")
    f.write(txt)
    f.close()
    #print(txt)
    drawing = svg2rlg(filename)
    pngname = filename.replace(".tmp", ".jpg")
    renderPM.drawToFile(drawing, pngname, 'JPEG')
    x = imread(pngname)
    img = cvtColor(x, COLOR_BGR2RGB)
    return img


def make_hokkaido_heatmap(filename, title, npa1d):
    """ 北海道のヒートマップを作成する """
    plt.close()
    plt.style.use("dark_background")
    #plt.subplots_adjust(left=0.07, right=0.99, bottom=0.07, top=0.95)
    plt.title(title, fontname=FONT_NAME)
    plt.rcParams['figure.figsize'] = 8, 8
    cmap = plt.get_cmap("rainbow")
    norm = plt.Normalize(vmin=np.min(npa1d), vmax=np.max(npa1d))
    fcol = lambda x: '#' + bytes(cmap(norm(x), bytes=True)[:3]).hex()
    plt.colorbar(cm.ScalarMappable(norm, cmap))
    map_cols = {}
    for k, v in sub_prefs.items():
        map_cols[k] = fcol(npa1d[k])
    #print(map_cols)
    pict = get_hokkaido(map_cols)
    plt.imshow(pict)
    plt.savefig(filename)


def test_picture():
    """ テスト """
    f = get_hokkaido({
        1:"#0000ff",
        2:"#ff0000",
        3:"#00ff00",
        4:"#ff00ff",
        5:"#00ffff",
        6:"#ffff00",
        7:"#ffffff",
        8:"#cccccc",
        9:"#000080",
        10:"#008000",
        11:"#800000",
        12:"#000000",
        13:"#800080",
        14:"#808000"
    })

    import matplotlib.pyplot as plt
    plt.imshow(f)
    plt.savefig("hoge.jpg")


if __name__ == "__main__":

    for k, v in sub_prefs.items():
        print("no:{} name:{} code:{} total:{} ".format(k, v['name'], v['code'], v['total']))

    for k, v in city_towns.items():
        print("k:{} v:{}".format(k, v))

    names = ["函館市", "旭川市", "白糠町", "小樽市", "空知", "日高", "日高振興局管内", "札幌市", "非公表", "中国"]
    for n in names:
        print("{} = {}".format(n, get_sub_code(n)))

    test_picture()
