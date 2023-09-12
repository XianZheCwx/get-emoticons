# -*- coding: utf-8 -*-

from scrapy.cmdline import execute

# 通过程序启动 spiders 项目
if __name__ == '__main__':
    execute(["scrapy", "crawl", "DouTuLa"])     # 启动 DouTuLa 工程
