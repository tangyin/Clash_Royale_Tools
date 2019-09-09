# coding=utf-8

import re
import requests
from bs4 import BeautifulSoup
from tools import *
import threading
import time

GTO_ID = "G22CY890"
XIAOBO_ID = "2Q9GC89GP"

PLAYER_API = "https://royaleapi.com/player/"
CLAN_API = "https://royaleapi.com/clan/"

interval_sb = 1800  # 每30分钟检查一次
interval_self = 43200  # 每12小时检查自身定时器的健康状态

data = [
    {
        "player_id": "2Q9GC89GP",
        "sb_name": "小波",
        "clan_id": "", "clan_qq": "", "clan_weixin": "", "clan_num": "",
        "show_msg": "", "need_mail": False
    },
    {
        "player_id": "G22CY890",
        "sb_name": "GTO_Brand",
        "clan_id": "", "clan_qq": "", "clan_weixin": "", "clan_num": "",
        "show_msg": "", "need_mail": False
    }
]


def get_clan_info(clan_id, each_user):
    url = CLAN_API + clan_id
    # print('clan info api', url)
    html = requests.get(url).content
    soup = BeautifulSoup(html, "html.parser")
    res = soup.find('div', class_="ui attached container sidemargin0 content_container").find_all('div', class_='value')
    for item in res:
        if '/' in item.string:
            each_user["clan_num"] = item.text
            # print('current member', item.text)


def _fuck_user(player_id, name, each_user):
    url = PLAYER_API + player_id
    html = requests.get(url).content
    soup = BeautifulSoup(html, "html.parser")
    res = soup.find('div', id='page_content_container').find_all('div', class_='ui header item')
    for item in res:
        tribe_link = item.find('a')
        if tribe_link:
            link_str = tribe_link['href']
            clan_id = link_str.split('/')[2]
            each_user["clan_id"] = clan_id
            each_user["clan_num"] = get_clan_current_member_num(clan_id, CLAN_API)
            each_user["clan_qq"] = try_get_qq(clan_id, CLAN_API)
            each_user["show_msg"] = "SB名：" + each_user["sb_name"] + "（" + each_user["player_id"] + ")" + \
                                    " 部落ID：" + each_user["clan_id"] + \
                                    " 部落QQ群：" + each_user["clan_qq"] + \
                                    " 部落人数：" + each_user["clan_num"] + '\n' + \
                                    "尝试使用以下模板发送QQ邮件给首领：" + '\n' + \
                                    "你好，XXX部落的首领，" + '\n' + \
                                    "我是部落clat 的首领，你的新部落成员：XXX曾在我们部落把所有成员踢出部落，如下是截图：" + '\n'
            if (int(each_user["clan_num"]) < 50) | (each_user["clan_qq"] != '检索不到QQ'):
                each_user["need_mail"] = True


def analysis_data():
    for each_user in data:
        _fuck_user(each_user["player_id"], "XXX", each_user)


def prepare_msg():
    message = ""
    for each_user in data:
        message = message + each_user["show_msg"] + '\n'
    return message


def check_sb():
    analysis_data()
    mail_body = ""
    for each_user in data:
        if each_user["need_mail"] is True:
            mail_body = mail_body + each_user["show_msg"]
    send_mail(mail_body)


def health_check():
    send_mail("Check SB Python服务正在运行中...")


def main():
    # check_sb()
    threading.Timer(interval_sb, check_sb).start()
    threading.Timer(interval_self, health_check).start()


if __name__ == "__main__":
    main()
