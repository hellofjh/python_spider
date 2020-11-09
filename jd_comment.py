# -*- coding: UTF-8 -*-
import collections # 词频统计库
import requests
import time
import json
import re
import pkuseg
import ctypes
import pyecharts.options as opts
from pyecharts.charts import WordCloud
from pyecharts.globals import SymbolType

class JD_bad():
    def __init__(self):
        self.link = "https://club.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98&productId=100016034400&score=3&sortType=5&page={}&pageSize=10&isShadowSku=0&rid=0&fold=1"
        self.filePath = './contents.txt'
        self.header = {}
        self.batch()

    def run(self, page):
        response = requests.get(page, headers=self.header)

        start_index = response.text.index('(')+1 #左边第一个括号开始
        _str = response.text[start_index:-2] #提取正确的json格式字符串
        try:
            _json = json.loads(_str)
        except:
            return False
        if 'comments' in _json.keys():
            for com_list in _json['comments']:
                content = com_list['content']
                return content
        return False

    def batch(self):
        contents_list = []
        for sum in range(0, 100): #100页
            page = self.link.format(sum)
            try_sum = 1
            while try_sum <= 5: #如果该页请求失败，重复5次后还失败则跳过
                content = self.run(page=page)
                if content is False:
                    try_sum += 1
                    time.sleep(1.5)
                    continue
                contents_list.append(content)
                break
        # 将所有评论存到文本
        with open(self.filePath, 'a+', encoding='utf-8') as file:
            file.writelines(contents_list)

    def make_str(self):
        with open(self.filePath, 'r', encoding='utf-8') as file:
            string_data = file.read()
            file.close()

            stop_word = open("drop.txt", "r", encoding='UTF-8').read().split("\n")
            for drop_str in stop_word:
                if drop_str in string_data:
                    string_data = string_data.replace(drop_str, "")

            seg = pkuseg.pkuseg()
            pkuseg_list = seg.cut(string_data)  # 进行分词

            new_list = []
            for str in pkuseg_list:
                if len(str) <= 1:
                    continue
                new_list.append(str)

            word_counts = collections.Counter(new_list)  # 对分词做词频统计
            word_counts_top500 = word_counts.most_common(500)  # 获取前500最高频的词
            # print(word_counts_top500)

            return word_counts_top500


if __name__=="__main__":
    _class = JD_bad()
    data = _class.make_str()
    WordCloud()\
        .add(
            "",
            data,
            word_size_range=[10, 85],
            textstyle_opts=opts.TextStyleOpts(font_family="汉仪雅酷黑简"),
        ).set_global_opts(
            title_opts=opts.TitleOpts(
                title="热点分析", title_textstyle_opts=opts.TextStyleOpts(font_size=23)
            ),
            tooltip_opts=opts.TooltipOpts(is_show=True),
        ).render("basic_wordcloud.html", width=1400, height=1000)