#!/usr/bin/env python
# coding: utf-8
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
f = "city_of_hokkaido.svg"
d = svg2rlg(f)
renderPM.drawToFile(d, f.replace("svg", "png"), fmt="PNG")
