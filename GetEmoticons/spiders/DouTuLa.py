# -*- coding: utf-8 -*-
import re
import scrapy

# 自定义模块结构
from GetEmoticons.common import DouTuLaPage
from GetEmoticons.settings import USER_AGENT
from GetEmoticons.items import GetemoticonsItem
from GetEmoticons.tools import (re_extract, now, print_news, c_print, url_param_splicing,
                                judg_yn, user_input)


class DoutulaSpider(scrapy.Spider):
    # 爬虫文件名称：当前源文件的唯一标识
    name = 'DouTuLa'
    # 允许的域名，可以注释，既下方的请求全部通过
    # allowed_domains = ['https://www.doutula.com/photo/list/']
    # 起始的url列表：只可以存储url，都会被进行get请求的发送
    headers = {
        "User-Agent": USER_AGENT
    }
    home_urls = r'https://www.doutula.com/photo/list/'
    # start_urls = ['https://www.doutula.com/photo/list/']

    """基础属性方法部分"""

    def start_requests(self):

        yield scrapy.Request(url=self.home_urls, headers=self.headers, callback=self.parse)

    def parse(self, response):
        max_pages = response.xpath(DouTuLaPage.max_pages).extract_first().strip()
        max_pages = int(max_pages)
        target_range = self.choose_page(max_pages)

        if isinstance(target_range, int):
            c_print(f"正在解析第{target_range}页")
            yield self.image_request(pages=target_range)
        elif isinstance(target_range, dict):
            target_type = target_range.get("type")
            data = target_range.get("pages")
            if target_type == "range":
                min_p, max_p = data
                for i in range(min_p, max_p):
                    c_print(f"正在解析第{i}页")
                    yield self.image_request(pages=i)
            else:
                for i in data:
                    c_print(f"正在解析第{i}页")
                    yield self.image_request(pages=i)

    """斗图啦表情包解析部分"""

    def image_request(self, pages=1):
        params = {
            "page": pages
        }
        url = url_param_splicing(self.home_urls, params)
        return scrapy.Request(url, headers=self.headers, callback=self.image_parse, meta={"pages": pages})

    def image_parse(self, response):
        target_range = response.xpath(DouTuLaPage.image_range)
        for i in target_range:
            details_url = i.xpath(r"./@href").extract_first()
            yield scrapy.Request(
                url=details_url,
                callback=self.image_details_parse,
                meta={"pages": response.meta["pages"]}
            )

    def image_details_parse(self, response):
        item = GetemoticonsItem()
        taget_range = response.xpath(r"//li[@class='list-group-item' and @style]")
        target_img = taget_range.xpath(DouTuLaPage.img)
        item["title"] = target_img.xpath(r"./@alt").extract_first() or None
        item["img_url"] = target_img.xpath(r"./@src").extract_first()
        item["img_info"] = re_extract(r".*/(.*)$", item['img_url'], flags="re.I")
        img_date = taget_range.xpath(DouTuLaPage.img_date).extract_first()

        if rule := re_extract(r"^(\d+-\d+-\d+)$", img_date):
            item["img_date"] = rule
        else:
            item["img_date"] = now()

        item["pages"] = response.meta["pages"]
        item["extract_date"] = now()
        yield item

    """辅助属性方法部分"""

    @staticmethod
    def choose_page(max_pages):
        while True:
            enter = user_input("请选择需要爬取的页数, 直接回车代表一页:",
                               hint_text=f"{'='*30}\n现发现本站点共有: {max_pages}分页\n{'︾'*18}")
            if enter:
                if enter.isdigit():
                    enter = int(enter)
                    if max_pages >= enter >= 1:
                        return enter
                    else:
                        c_print(f"请输入符合 1-{max_pages}之间的值")

                elif rule := re.match(r"(\d+)-(\d+)$", enter):
                    min_p, max_p = [int(i) for i in rule.groups()]
                    if max_pages >= max_p >= 1:
                        return {"type": "range", "pages": [min_p, max_p+1]}
                    else:
                        c_print(f"请输入符合 1-{max_pages}之间的值")

                elif re.match(r"(\d+,|，(\d+)?)+", enter):
                    res = []
                    for i in re.split(r",|，", enter):
                        if i.isdigit():
                            res.append(int(i))
                    res.sort()

                    if int(max_pages) >= res[-1] >= 1:
                        return {"type": "target_range", "pages": res}
                else:
                    c_print("识别错误", c_id=31)
            else:
                c_print("输入不能为空", c_id=31)
