# 全国 新型コロナ予測

{% include plotly.html %}

## 倍加時間（累乗近似）
{% include mhlw-doubling-time.html %}

{% include mhlw-fit.html %}

※近似式は以下を使用。倍加時間 $ d $ は $ d = 1 / b $ で計算可能。


\\[
y = a 2^{b x} + c
\\]

## 陽性者数/陽性率

{% include mhlw-posis.html %}

## 検査人数/陽性率

{% include mhlw-tests.html %}

## 経路不明率

{% include mhlw-total.html %}

## 実効再生産数

{% include ogiwara-ern.html %}
