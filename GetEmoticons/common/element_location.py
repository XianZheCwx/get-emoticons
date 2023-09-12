# -*- coding: utf-8 -*-


class DouTuLaPage:
    # 最大页数定位
    max_pages = r"//div[@id='pic-detail']/div/div[2]/div[3]/ul/li[12]/a/text()"
    # 表情包范围
    image_range = r"//li[@class='list-group-item']/div[@class='page-content text-center']/div/a"
    # 表情包地址
    img = r".//div[@class='col-xs-12 col-sm-12 artile_des']//img[@referrerpolicy='no-referrer']"
    # 表情包日期
    img_date = r".//span[@class='glyphicon glyphicon-time']/text()"




