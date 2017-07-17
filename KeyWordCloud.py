# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import jieba
import wordcloud
from wordcloud import WordCloud, STOPWORDS


houseinfo = pd.read_csv('D:\\Python Script\\WebCrawler\\Housedata\\testing.csv', index_col = 0 )
text = ' '
for contents in houseinfo['title'].values:
    text = text + contents



seg = jieba.cut(text)
ChineseText = " ".join(seg)


coloring = plt.imread('D:\\Python Script\\PythonWithFun\\WordCloud\\spider.jpg')

wc = WordCloud(font_path = 'D:\\Python Script\\PythonWithFun\\WordCloud\\msyhbd.ttf',
               width=800, height=400,
               max_words=2000,
               background_color="white", #背景颜色max_words=2000,# 词云显示的最大词数
               mask = coloring, #设置背景图片
               stopwords=STOPWORDS.add('said'),
               max_font_size=40, #字体最大值
               random_state=42) #font_path = 'D:\\Python Script\\PythonWithFun\\WordCloud\\msyhbd.ttf',


wc.generate(ChineseText)


image_colors = wordcloud.ImageColorGenerator(coloring)

plt.figure(figsize=(20,10))
plt.imshow(wc.recolor(color_func= image_colors, random_state=3), interpolation='bilinear')
plt.axis("off")
plt.savefig('D:\\Python Script\\PythonWithFun\\WordCloud\\houseinfo.jpg')
plt.show()
