#coding=utf-8

import re
import requests
from bs4 import BeautifulSoup


GTO_ID = "G22CY890"
XIAOBO_ID = "2Q9GC89GP"

PLAYER_API = "https://royaleapi.com/player/"
TRUBE_API = "https://royaleapi.com/clan/"



def get_clan_info(clan_id):
    url = TRUBE_API + clan_id
    print('clan info api', url)
    html = requests.get(url).content
    soup = BeautifulSoup(html, "html.parser")
    res = soup.find('div', class_="ui attached container sidemargin0 content_container").find_all('div', class_='value')
    for item in res:
        if '/' in item.string:
            print('current member', item.text)


def get_clan_description(clan_id):
    clan_url = TRUBE_API + clan_id
    html = requests.get(clan_url).content
    soup = BeautifulSoup(html, "html.parser")
    res = soup.find('meta', property="og:description")['content']
    print(res)
    _analysis_msg(res)
    return res


def _analysis_msg(clan_description):
    # Try find qq number
    # First find string of qq
    string_qq_index = clan_description.lower().find('qq')
    if string_qq_index != -1:
        print(string_qq_index)
        print('Find qq')
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
        print(after_qq_string_array)
        print(qq_number)
        return qq_number


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

def main():
    get_clan_description('PPPP0JCQ')
    #fuck_xiaobo()
    #print("====="*4)
    #fuck_gto_brand()




if __name__ == "__main__":
    main()




