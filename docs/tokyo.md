# 東京都 新型コロナ予測
{% include plotly.html %}

## 倍加時間 (累乗近似)

{% include tokyo-doubling-time.html %}

{% include tokyo-fit.html %}

※近似式は以下を使用。倍加時間 $ d $ は $ d = 1 / b $ で計算可能。

\\[
y = a 2^{b x} + c
\\]

## 新規感染者数
※気象業務法第13～24条に接触するため、予報を含まない前日までの気温データのみを表示（気象データに関する予報値を含まない）。

{% include tokyo.html %}

## 検査人数/陽性率
{% include tokyo-rate.html %}

## 経路不明率
{% include tokyo-track.html %}

## 全期間 罹患率 
{% include tokyo-hm.html %}
