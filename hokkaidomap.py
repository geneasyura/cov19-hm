#!/usr/bin/python3
# coding: utf-8
# This source code is based on japanmap: https://github.com/SaitoTsutomu/japanmap

import codecs
from cv2 import imread
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
from pathlib import Path

sub_prefs = [
     dict(name=""          , code="00", suffix="変更なし"  ),
     dict(name="石狩"      , code="01", suffix="振興局"    ),
     dict(name="渡島"      , code="02", suffix="総合振興局"),
     dict(name="桧山"      , code="03", suffix="振興局"    ),
     dict(name="後志"      , code="04", suffix="総合振興局"),
     dict(name="空知"      , code="05", suffix="総合振興局"),
     dict(name="上川"      , code="06", suffix="総合振興局"),
     dict(name="留萌"      , code="07", suffix="振興局"    ),
     dict(name="宗谷"      , code="08", suffix="総合振興局"),
     dict(name="オホーツク", code="09", suffix="総合振興局"),
     dict(name="胆振"      , code="10", suffix="総合振興局"),
     dict(name="日高"      , code="11", suffix="振興局"    ),
     dict(name="十勝"      , code="12", suffix="総合振興局"),
     dict(name="釧路"      , code="13", suffix="総合振興局"),
     dict(name="根室"      , code="14", suffix="振興局"    )
]

#pref_names = (
#    "_ 北海道 青森県 岩手県 宮城県 秋田県 山形県 福島県 茨城県 栃木県 "
#    "群馬県 埼玉県 千葉県 東京都 神奈川県 新潟県 富山県 石川県 福井県 山梨県 "
#    "長野県 岐阜県 静岡県 愛知県 三重県 滋賀県 京都府 大阪府 兵庫県 奈良県 "
#    "和歌山県 鳥取県 島根県 岡山県 広島県 山口県 徳島県 香川県 愛媛県 高知県 "
#    "福岡県 佐賀県 長崎県 熊本県 大分県 宮崎県 鹿児島県 沖縄県"
#).split()
#pref_ = {s.rstrip("都道府県"): i for i, s in enumerate(pref_names)}
#pref = {s: i for i, s in enumerate(pref_names)}
#groups = {
#    "北海道": [1],
#    "東北": [2, 3, 4, 5, 6, 7],
#    "関東": [8, 9, 10, 11, 12, 13, 14],
#    "中部": [15, 16, 17, 18, 19, 20, 21, 22, 23],
#    "近畿": [24, 25, 26, 27, 28, 29, 30],
#    "中国": [31, 32, 33, 34, 35],
#    "四国": [36, 37, 38, 39],
#    "九州": [40, 41, 42, 43, 44, 45, 46, 47],
#}

def get_svg_txt(dic=None, rate=1):
    f = codecs.open(str(Path(__file__).parent / "Subprefectures_of_Hokkaido.svg"), encoding="utf-8")
    p = f.read()
    if hasattr(dic, "items"):
        for k, v in dic.items():
            i = k if isinstance(k, int) else int(k.lstrp("0"))
            if 1 <= i <= 14:
                p = p.replace("#c%02d" % (k), v)
    return p

def get_hokkaido(dic=None, ret=1):
    txt = get_svg_txt(dic, ret)
    filename = str(Path(__file__).parent / "svglib.tmp")
    f = codecs.open(filename, "w", encoding="utf-8")
    f.write(txt)
    f.close()
    drawing = svg2rlg(filename)
    pngname = filename.replace(".tmp", ".jpg")
    renderPM.drawToFile(drawing, pngname, 'JPEG')
    x = imread(pngname)
    return x

def test_picture():
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
    test_picture()
