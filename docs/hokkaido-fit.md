# 北海道 新型コロナウィルス

{% include plotly.html %}

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
