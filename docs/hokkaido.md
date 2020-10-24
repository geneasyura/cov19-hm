# 北海道 新型コロナウィルス 状況及び予測

{% include plotly.html %}

## 新規感染者数
{% include hokkaido.html %}

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
