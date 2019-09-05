#coding=utf-8

import re
import requests
from bs4 import BeautifulSoup
from tools import *

GTO_ID = "G22CY890"
XIAOBO_ID = "2Q9GC89GP"

PLAYER_API = "https://royaleapi.com/player/"
TRUBE_API = "https://royaleapi.com/clan/"

data = [
    {
        "player_id": "2Q9GC89GP",
        "sb_name": "小波",
        "clan": "", "clan_qq": "", "clan_weixin": ""
    },
    {
        "player_id": "G22CY890",
        "sb_name": "GTO_Brand",
        "clan": "", "clan_qq": "", "clan_weixin": ""
    }
]



def get_clan_info(clan_id):
    url = TRUBE_API + clan_id
    print('clan info api', url)
    html = requests.get(url).content
    soup = BeautifulSoup(html, "html.parser")
    res = soup.find('div', class_="ui attached container sidemargin0 content_container").find_all('div', class_='value')
    for item in res:
        if '/' in item.string:
            print('current member', item.text)


def _fuck_user(player_id, name):
    url = PLAYER_API + player_id
    print('player info api', url)
    html = requests.get(url).content
    soup = BeautifulSoup(html, "html.parser")
    res = soup.find('div',id='page_content_container').find_all('div', class_='ui header item')
    for item in res:
        tribe_link = item.find('a')
        if tribe_link:
            link_str = tribe_link['href']
            tribe_id = link_str.split('/')[2]
            print('%s clan id is'%name, tribe_id)
            get_clan_info(tribe_id)

def fuck_xiaobo():
    _fuck_user(XIAOBO_ID, 'xiaobo')

def fuck_gto_brand():
    _fuck_user(GTO_ID, 'GTO_brand')

def load_data():
    for each_user in data:
        print(each_user["player_id"])

def show_data():
    for each_user in data:
        print(each_user["sb_name"] + "（" + each_user["player_id"] + ")")
        print("当前部落名：" + each_user["clan"] + " 部落QQ群：" + each_user["clan_qq"])


def main():
    load_data()
    show_data()
    #get_clan_description('PPPP0JCQ')
    #fuck_xiaobo()
    #print("====="*4)
    #fuck_gto_brand()




if __name__ == "__main__":
    main()




