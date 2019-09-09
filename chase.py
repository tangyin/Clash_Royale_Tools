#coding=utf-8

import re
import requests
from bs4 import BeautifulSoup
from tools import *

GTO_ID = "G22CY890"
XIAOBO_ID = "2Q9GC89GP"

PLAYER_API = "https://royaleapi.com/player/"
CLAN_API = "https://royaleapi.com/clan/"

data = [
    {
        "player_id": "2Q9GC89GP",
        "sb_name": "小波",
        "clan": "", "clan_id": "", "clan_qq": "", "clan_weixin": "", "clan_num": ""
    },
    {
        "player_id": "G22CY890",
        "sb_name": "GTO_Brand",
        "clan": "", "clan_id": "", "clan_qq": "", "clan_weixin": "", "clan_num": ""
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


def fuck_xiaobo():
    _fuck_user(XIAOBO_ID, 'xiaobo')


def fuck_gto_brand():
    _fuck_user(GTO_ID, 'GTO_brand')


def analysis_data():
    for each_user in data:
        _fuck_user(each_user["player_id"], "XXX", each_user)


def show_data():
    message = ""
    for each_user in data:
        message = message + "SB名：" + each_user["sb_name"] + "（" + each_user["player_id"] + ")" + \
              " 部落名：" + each_user["clan"] + \
              " 部落ID：" + each_user["clan_id"] + \
              " 部落QQ群：" + each_user["clan_qq"] + \
              " 部落人数：" + each_user["clan_num"] + '\n'
        print("SB名：" + each_user["sb_name"] + "（" + each_user["player_id"] + ")" +
              " 部落名：" + each_user["clan"] +
              " 部落ID：" + each_user["clan_id"] +
              " 部落QQ群：" + each_user["clan_qq"] +
              " 部落人数：" + each_user["clan_num"])
    send_mail(message)


def main():
    analysis_data()
    show_data()
    #get_clan_description('PPPP0JCQ')
    #fuck_xiaobo()
    #print("====="*4)
    #fuck_gto_brand()




if __name__ == "__main__":
    main()




