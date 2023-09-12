# -*- coding: utf-8 -*-
import os
import re
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus'] = False

BASE_DIR = os.path.dirname(__file__)
INFO_DIR = os.path.join(BASE_DIR, "info")


def judg_dir(func):
    def inner(*args, **kwargs):
        if not os.path.isdir(INFO_DIR):
            raise Exception("info目录未生成, 请先爬取数据")
        ret = func(*args, **kwargs)
        return ret
    return inner


class ShowPic:
    def __init__(self, file_name):
        if os.path.isabs(file_name):
            self.file_path = file_name
        else:
            self.file_path = os.path.join(INFO_DIR, file_name)

    @judg_dir
    def load_data(self):
        df = pd.read_csv(self.file_path, sep=",", encoding="gbk")
        return df

    @staticmethod
    def extract_data(dataframe):
        new_date = []
        for i in dataframe["img_date"].tolist():
            if rule := re.match(r"^(\d+[/-]\d+)[/-]\d+", i):
                new_date.append(rule.group(1))
        dataframe["date"] = new_date
        group_date = dataframe.groupby("date")
        counts = group_date.count()
        g_dates = counts.index.tolist()
        g_count = counts["title"].tolist()
        return dict(zip(g_dates, g_count))

    def draw_pie(self, title):
        data = self.extract_data(self.load_data())
        lables = list(data.keys())
        plt.pie(
            list(data.values()),
            labels=lables,
            shadow=True,
            autopct="%1.1f%%"
        )
        plt.title(title)
        plt.legend(
            lables,
            title="饼图图例",
            loc="best",
            # 控制图例中按照两列显示，默认为一列显示
            ncol=2,
           )
        plt.tight_layout()
        plt.show()


if __name__ == '__main__':
    Show = ShowPic("爬虫爬取记录文件.csv")
    Show.draw_pie("斗图啦爬取图片日期统计")

