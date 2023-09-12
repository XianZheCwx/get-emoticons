# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import os
import csv
import scrapy
import pymysql

from GetEmoticons import settings
from itemadapter import ItemAdapter
from scrapy.utils.misc import md5sum
from scrapy.pipelines.images import ImagesPipeline


from GetEmoticons.tools import re_extract
from GetEmoticons.db_models import MySQL


# class GetemoticonsPipeline:
#
#     def open_spider(self, spider):
#         pass
#
#     def close_spider(self, spider):
#         pass
#
#     def process_item(self, item, spider):
#         return item


class LocalPipeline:
    file_name = None
    file_path = None
    header = ['title', 'img_url', 'img_info', 'img_date', 'extract_date', 'page']

    def open_spider(self, spider):
        self.file_name = "爬虫爬取记录文件.csv"
        self.file_path = os.path.join(settings.INFO_DIR, self.file_name)
        if not os.path.isdir(settings.INFO_DIR):
            os.mkdir(settings.INFO_DIR)

        if not os.path.isfile(os.path.join(settings.INFO_DIR, self.file_name)):
            with open(self.file_path, "w") as f_w:
                f_w.write(f"{','.join(self.header)}\n")

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        save_data = [
            item["title"], item["img_url"], item["img_info"], item["img_date"],
            item["extract_date"], item["pages"]
        ]
        save_data = ",".join([str(i) for i in save_data])
        with open(self.file_path, "a") as f_a:
            f_a.write(f"{save_data}\n")
        return item


class MysqlPipeline:
    mysql = None

    def open_spider(self, spider):
        self.mysql = MySQL("doutula")

    def close_spider(self, spider):
        self.mysql.close()

    def process_item(self, item, spider):
        self.mysql.insert(item)
        return item


class ImgDownloadPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        img_url = item["img_url"]
        yield scrapy.Request(url=img_url, meta={"item": item})

    def file_path(self, request, response=None, info=None, *, item=None):
        if ((img_name := item["title"]) is not None) and (img_name not in ["?", r"\\", r"/", r"*", "|"]):
            img_name = re_extract(r"(.*/)*(.*)$", img_name, which=2)
            suffix = re_extract(r".*(\..*)$", item["img_info"], flags="re.I")
            img_name = f"{img_name}{suffix}"
            return img_name
        else:
            return item["img_info"]

    def image_downloaded(self, response, request, info, *, item=None):
        checksum = None
        for path, image, buf in self.get_images(response, request, info, item=item):
            if checksum is None:
                buf.seek(0)
                checksum = md5sum(buf)
            width, height = image.size
            if self.__isfig(image.format):
                self.__download_gif(path, response.body, info)
            else:
                self.store.persist_file(
                    path, buf, info,
                    meta={'width': width, 'height': height},
                    headers={'Content-Type': 'image/jpeg'})
        return checksum

    @staticmethod
    def __isfig(img_format):
        if img_format is None or img_format == "GIF":
            return True

    def __download_gif(self, path, gif_date, info):
        root, ext = os.path.splitext(path)
        gif_path = self.store._get_filesystem_path(path)
        self.store._mkdir(os.path.dirname(gif_path), info)
        with open(gif_path, "wb") as f_w:
            f_w.write(gif_date)

    def item_completed(self, results, item, info):
        return item

