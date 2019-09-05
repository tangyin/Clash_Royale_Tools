#coding=utf-8

import re
import requests
from bs4 import BeautifulSoup


def try_get_qq(clan_description):
    # Try find qq number
    # First find string of qq
    string_qq_index = clan_description.lower().find('qq')
    if string_qq_index != -1:
        # print(string_qq_index)
        # print('Find qq')
        # 有时候公告会写成：QQ群是XXX，qq字符串后面的XXX会跟着中文或者非数字，不会直接就是QQ号或者微信号，
        # 所以必须从qq字符开始找到第一个数字
        after_qq_string_array = clan_description[string_qq_index:]
        qq_number = ''
        for each_string in after_qq_string_array:
            if each_string.isnumeric():
                qq_number = qq_number + each_string
            else:
                # 如果匹配到的不是数字，并且qq号已经开始拼接，代表已经拼接完了。循环可以退出
                # 例如： QQ群： 1234567 10个人现在
                # 当前拼接的qq号为：1234567，当前字符串为『空格』，则不应该继续拼接后面的1（0个人现在）
                if qq_number.isnumeric():
                    break
        # print(after_qq_string_array)
        # print(qq_number)
        return qq_number


def get_clan_description(clan_id, trube_api):
    clan_url = trube_api + clan_id
    html = requests.get(clan_url).content
    soup = BeautifulSoup(html, "html.parser")
    res = soup.find('meta', property="og:description")['content']
    return res
