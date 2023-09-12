# -*- coding: utf-8 -*-
import re
import pymysql

from GetEmoticons.settings import DATABASES


class MySQL:
    # MYSQL 数据库处理类
    def __init__(self, table: str):
        self.databases = self.__init_coding(DATABASES)
        self.comm = self.__link()
        self.table = table.lower()
        if not self.__judg_table():
            self.create_table()

    def show_tables(self) -> list:
        """
        查看当前库中的表
        :return: 以列表形式放回库中列表
        """
        cursor = self.comm.cursor()
        sql = r"show tables"
        cursor.execute(sql)
        ret = [i[0].lower() for i in cursor.fetchall()]
        cursor.close()
        return ret

    def insert(self, dic: dict, length=6):
        """
        向Mysql中插入数据
        :param dic: 以字典形式将数据传入
        :param length: 数据内容长度, 默认为6
        """
        if not isinstance(dic, dict) and len(dic) != length:
            err("传入参数错误")

        cursor = self.comm.cursor()
        sql = fr"""
        INSERT INTO {self.table}
            (title, img_url, img_info, img_date, extract_date, page) VALUES
            (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(
            sql, (
                dic["title"], dic["img_url"], dic["img_info"], dic["img_date"],
                dic["extract_date"], dic["pages"]
            ))
        self.comm.commit()
        cursor.close()

    def create_table(self):
        """
        创建初始表
        """
        cursor = self.comm.cursor()
        sql = rf"""
        CREATE TABLE {self.table} (
            id INT unsigned PRIMARY KEY auto_increment,
            title char(100),
            img_url char(180) not null,
            img_info char(200),
            img_date char(25),
            extract_date char(25),
            page MEDIUMINT unsigned
        )
        """.strip()
        cursor.execute(sql)

    def close(self):
        self.comm.close()

    def __judg_table(self):
        tables = self.show_tables()
        return tables and self.table in tables

    @staticmethod
    def __init_coding(databases):
        if rule := re.match(r"^utf-8$", databases["CODING"], re.I):
            databases["CODING"] = rule.group().replace("-", "")
        return databases

    def __link(self):
        databases = self.databases
        comm = pymysql.connect(
            host=databases["HOST"],
            port=databases["PORT"],
            user=databases["USER"],
            password=databases["PASSWORD"],
            db=databases["DB"],
            charset=databases["CODING"]
        )
        return comm


# if __name__ == '__main__':
#     mysql = MySQL("DouTuLa")
#     print(mysql.show_tables())
#     mysql.insert({"title": "6", "img_url": "6", "img_info": "6", "img_date": "6", "extract_date": 6, "page": 6})



