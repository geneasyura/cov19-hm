# 北海道 新型コロナウィルス

{% include plotly.html %}

## 感染日と気温/絶対湿度の関係性

感染日の気温・絶対湿度の関係について考える。

各日で報告される新規感染者数、札幌の平均気温、絶対湿度の値を使用するが、
データ均質化のために7日移動平均値を使用する。
また、報告される各新規感染者者の感染日を特定することは難しいため、一律に
7.0日前(+潜伏2.5日+検査待2.5日+結果待+1.0日+集計公表+1.0日)とする。

$x$ 軸を札幌の平均気温の7日移動平均、$y$ 軸を絶対湿度の7日移動平均とし、
人数をカラースケールでプロットしたのが以下の図である。

{% include hokkaido-tvh-contour.html %}

本グラフは日毎に自動的に更新される。

平均気温が約10℃、絶対湿度が 7g/㎥を下回ると感染が拡大しているように見受けられる。

温湿度・気圧から計算される空気抵抗力もファクターの一つであるが、温湿度が重要なファクターのように見える。

10℃以下かつ6g/㎥以下のデータは2020年第一波（緊急事態宣言時）のものであるため、
本格的な冬のデータはまだ採取できていない。
現状ではインフルエンザ流行と同様の結果になると予測される。

絶対湿度とインフルエンザ流行については、例えば 1999 年の文献でも確認できる。
文献の内容をまとめると以下のようになる。

* 17g/㎥以上：ほとんどリスクなし
* 11g/㎥以上：ほぼリスクなし
* 7～11g/㎥ ：低リスク(注意報)
*  7g/㎥未満：中リスク(警報)
*  5g/㎥未満：高リスク(特別警報)

ただし、地域特性があり、北海道から宮城は 5g/㎥、鹿児島は 7g/㎥、東京・沖縄は 10g/㎥となっている。
緯度の違いによる重力加速度の差分が微粒子に影響するものと思われる。
北海道は東京よりも重力加速度が大きいため、微粒子が地表に落下する時間が早いものと思う。

### 相対湿度 [%RH] のグラフ

{% include hokkaido-trh-contour.html %}


## 参考資料

* J.min様: [Aerosol Influenza Transmission Risk Contours](https://twitter.com/Jmin123456789/status/1322731083641712641)
* J.min様: [絶対湿度とCOVID19の再生産数R0の関係](https://twitter.com/Jmin123456789/status/1322594498895962112)
* J.min様: [各国の通年絶対湿度](https://twitter.com/Jmin123456789/status/1315690033135845382)
* J.min様: [絶対湿度の流行条件](https://twitter.com/Jmin123456789/status/1315682303796940805)
* 庄司 眞: [季節とインフルエンザの流行](https://www.niph.go.jp/journal/data/48-4/199948040003.pdf). 1999.
* [Temperature, Humidity, and Latitude Analysis to Estimate Potential Spread and Seasonality of Coronavirus Disease 2019 (COVID-19)](https://jamanetwork.com/journals/jamanetworkopen/fullarticle/2767010)
* [Wet-Bulb Temperature Modulates SARS-CoV-2 Superspreading Events](https://www.researchgate.net/publication/344819638_Wet-Bulb_Temperature_Modulates_SARS-CoV-2_Superspreading_Events)
* [COVID-19が疑われた場合の医療ケアにおける感染予防と制御 が疑われた場合の医療ケアにおける感染予防と制御 が疑われた場合の医療ケアにおける感染予防と制御 が疑われた場合の医療ケアにおける感染予防と制御 が疑われた場合の医療ケアにおける感染予防と制御 が疑われた場合の医療ケアにおける感染予防と制御](https://extranet.who.int/kobe_centre/sites/default/files/translations/20200319_JA_IPC_Healthcare.pdf)
