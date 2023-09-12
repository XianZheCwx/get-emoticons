# -*- coding: utf-8 -*-
import re
import time

from hashlib import md5

# 自定义模块结构
from .exceptions import ParamTypeException


def c_print(text, c_id=32):
    if text:
        print(f"\033[1;{c_id}m{text}\033[0m")


def timer(func):
    """程序计时装饰器"""
    def inner(*args, **kwargs):
        start_time = time.time()
        ret = func(*args, **kwargs)
        time.sleep(1)
        print(f"运行时间为：{time.time() - start_time}")
        return ret
    return inner


def user_input(text, hint_text=None, **kwargs):
    """
    用户输入辅助函数
    :param text: input输入提示
    :param hint_text: 打印提示信息内容
    """
    if hint_text is not None:
        c_print(hint_text, **kwargs)
    return input(text).strip()


def re_extract(pattern, string, flags=None, which=1):
    """
    正则提取内容辅助函数
    :param pattern: 正则表达式
    :param string: 字符串内容
    :param flags: 修饰符
    :param which: 提取第几个, 默认为1
    :return: 提取的内容或None
    """
    if flags is not None and isinstance(flags, str):
        flags = flags.replace("re.", "")
        flags = getattr(re, flags)
    else:
        flags = 0
    if rule := re.match(pattern, string, flags=flags):
        return rule.group(which)


def judg_yn(*args, **kwargs):
    while True:
        enter = user_input(*args, **kwargs)
        if re.match(r"y$|yes$", enter, flags=re.I):
            return True
        elif re.match(r"n$|no$", enter, flags=re.I):
            return False
        c_print("输入错误, 请重新输入", c_id=31)


def now():
    """
    获取当前时间
    """
    return time.strftime("%Y/%m/%d %H:%M:%S")

# def get_maxpage(url, header):
#     """
#     获取最大页数辅助函数
#     :param url: url地址
#     :param header: 请求头
#     :return: 最大页数
#     """
#     response = requests.get(url, headers=header)
#     if response.ok:
#         response.encoding = "utf-8"
#         soup = BeautifulSoup(response.text, "html.parser")
#         target_range = soup.find("ul", class_="pagination")
#         max_page = target_range.select("li.page-item")[-2]
#         return max_page.text


def print_news(text, inp=False, inp_text=None):
    """
    打印信息辅助函数, 如需用户输入则需要 inp和inp_text 参数不为空
    :param text: 信息内容
    :param inp: 是否想要用户输入
    :param inp_text: 输入提示内容
    :return: 用户输入结果或空
    """
    c_print(text)
    if inp is True and inp_text is not None:
        return input(inp_text).strip()


def en_md5(data, coding="utf-8"):
    md5_obj = md5()
    md5_obj.update(str(data).encode(coding))
    return md5_obj.hexdigest()


def string_replace(olds, news, string):
    """
    字符串内容替换辅助函数
    :param olds: 旧字符串,可以是集
    :param news: 新字符串,可以是集合,但需要与旧字符串集长度一直
    :param string: 被替换字符串
    :return: 替换结果
    """
    if isinstance(olds, str) and isinstance(news, str):
        return string.replace(olds, news)
    elif isinstance(olds, (list, tuple)) and isinstance(news, str):
        pattern = "|".join([f"({i})" for i in olds])
        return re.sub(pattern, news, string)
    elif isinstance(olds, (list, tuple)) and isinstance(news, (list, tuple)):
        if len(olds) != len(news):
            raise IndexError("两者长度不一致")
        for o, n in zip(olds, news):
            string = string.replace(o, n)
        return string
    else:
        raise ParamTypeException


def url_param_splicing(url: str, params: dict):
    """网址请求参数拼接辅助函数

    Args:
        url: 原网址
        params: 请求参数
    Returns: 网址路径拼接结果
    """
    if not re.match(r".+\?$", url):
        url += "?"

    params_list = []
    for k, v in params.items():
        if v:
            params_list.append(f"{k}={v}")
    url += "&".join(params_list)
    return url
