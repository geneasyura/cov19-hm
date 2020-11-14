# 北海道 新型コロナウィルス 状況及び予測

{% include plotly.html %}

## 新規感染者数

### 空気抵抗力と新規感染者数

空気感染が主たる感染経路であると仮定し、N95マスクで大幅に暴露量を低減できることから、
新型コロナウィルスの微粒子直径 $L$ を 0.4 μm (平均微粒子半径 $R$ 0.2 μm ) とする。
また、簡単のため微粒子は球体であるとする。空気抵抗力 $F_d$、空気粘性率 $\eta$ [kg/ms]、
空気密度 $\rho$ [kg/m${}^3$]、球体速度 $v$ [m/s] を定義する。
呼気によって放出される球体速度 $v$ は 0.8 m/s とする。shikino 様による球体空気抵抗力の計算式を用い、
ウィルスを含む呼気から放出される微粒子に働く空気抵抗力と新規感染者数を以下に示す。
微粒子に働く空気抵抗力（温湿度・気圧）が弱ければ弱いほど、微粒子の動きが活発化し、感染拡大につながると予測する。
11月よりも12月、そして1月～2月がもっとも空気抵抗力が減少する。季節性インフルエンザ流行期と合致する。

{% include hokkaido-fd.html %}

### 気温と新規感染者数
※気象業務法第13～24条に接触するため、予報を含まない前日までの気温データのみを表示（気象データに関する予報値を含まない）。

{% include hokkaido.html %}

### 絶対湿度と新規感染者数
{% include hokkaido-ah.html %}

※平均気温[℃]を$t$、平均蒸気圧[hPa]を $p$、容積絶対湿度[g/㎥] $h$ を次式で計算。


\\[
h = 18.0 \times \frac{100.0 \times p} {8.31447 \times (273.15 + t)}
\\]


### 倍加時間 (累乗近似)

{% include hokkaido-doubling-time.html %}

{% include hokkaido-fit.html %}

※近似式は以下を使用。倍加時間 $ d $ は $ d = 1 / b $ で計算可能。


\\[
y = a 2^{b x} + c
\\]

### 移動平均 倍加時間 (累乗近似)

{% include hokkaido-doubling-time-ave.html %}

{% include hokkaido-fit-ave.html %}

## 検査人数/陽性率
{% include hokkaido-rate.html %}

## 検査人数/経路不明率

※経路不明率は簡易計算式「非濃厚接触者 / (濃厚接触者 + 非濃厚接触者)」を使用して算出。

{% include hokkaido-unknown.html %}

## 振興局別 罹患率[全期間] 
{% include hokkaido-all.html %}

## 振興局別 陽性者数(全期間)
{% include hokkaido-all-n.html %}

## 振興局別 実効再生産数(簡易計算)
{% include hokkaido-Rt.html %}

## 振興局別 直近2週間罹患率
{% include hokkaido-2w.html %}


## 参考資料

* shikino. [球体の空気抵抗と係数](https://slpr.sakura.ne.jp/qp/air-resistance/). 2015.
* 平原, 吉崎. [肺呼吸における流れと物質輸送](https://www.nagare.or.jp/download/noauth.html?d=34-4tokushu5.pdf&dir=144). ながれ34（2015）297-304.

