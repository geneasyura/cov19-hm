# 東京都 新型コロナ
{% include plotly.html %}

## 倍加時間 (累乗近似)

{% include tokyo-doubling-time.html %}

{% include tokyo-fit.html %}

※近似式は以下を使用。倍加時間 $ d $ は $ d = 1 / b $ で計算可能。

\\[
y = a 2^{b x} + c
\\]

## 移動平均を用いた倍加時間 (累乗近似)

{% include tokyo-doubling-time-ave.html %}

{% include tokyo-fit-ave.html %}
