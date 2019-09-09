#coding=utf-8

import re
from email.mime.text import MIMEText

import requests
import smtplib
from bs4 import BeautifulSoup


def try_get_qq(clan_id, clan_api):
    # Try find qq number
    # First find string of qq
    qq_number = ''
    clan_description = get_clan_description(clan_id, clan_api)
    string_qq_index = clan_description.lower().find('qq')
    if string_qq_index != -1:
        # print(string_qq_index)
        # print('Find qq')
        # 有时候公告会写成：QQ群是XXX，qq字符串后面的XXX会跟着中文或者非数字，不会直接就是QQ号或者微信号，
        # 所以必须从qq字符开始找到第一个数字
        after_qq_string_array = clan_description[string_qq_index:]
        for each_string in after_qq_string_array:
            if each_string.isnumeric():
                qq_number = qq_number + each_string
            else:
                # 如果匹配到的不是数字，并且qq号已经开始拼接，代表已经拼接完了。循环可以退出
                # 例如： QQ群： 1234567 10个人现在
                # 当前拼接的qq号为：1234567，当前字符串为『空格』，则不应该继续拼接后面的1（0个人现在）
                if qq_number.isnumeric():
                    break
    if qq_number is None:
        qq_number = "检索不到QQ"
    if qq_number == '':
        qq_number = "检索不到QQ"
    return qq_number


def get_clan_description(clan_id, clan_api):
    clan_url = clan_api + clan_id
    html = requests.get(clan_url).content
    soup = BeautifulSoup(html, "html.parser")
    res = soup.find('meta', property="og:description")['content']
    return res


# 部落总人数肯定是50人固定值
def get_clan_current_member_num(clan_id, clan_api):
    clan_url = clan_api + clan_id
    html = requests.get(clan_url).content
    soup = BeautifulSoup(html, "html.parser")
    res = soup.find('div', class_="ui attached container sidemargin0 content_container").find_all('div', class_='value')
    for item in res:
        if '/' in item.string:
            return item.text.split('/')[0]  # 返回数据类似： 37


######################################
# 1. 检索频率30分钟一次
######################################
def verify_need_mail(data):
    # current_member_num, has_qq, has_weichat
    # 达到以下条件，触发邮件通知
    # 1：部落人数小于50人（可以根据部落ID手动进入部落，联系首领）
    # OR
    # 2：检索到QQ号（根据QQ号，联系首领）
    # OR
    # 3：检索到微信号（根据微信号，联系首领）
    need_mail = False
    for each_user in data:
        if int(each_user["clan_num"]) < 50 | each_user["clan_qq"] != '检索不到QQ':
            need_mail = True
    return need_mail


def send_mail(mail_body):
    # 第三方 SMTP 服务
    mail_host = "smtp.163.com"  # SMTP服务器
    mail_user = "superman139"  # 用户名
    mail_pass = "fucksb123"  # 授权密码，非登录密码

    sender = "superman139@163.com"
    receivers = ['neosunchao@icloud.com', '361705773@qq.com']

    title = '干活啦，搞这两SB了'  # 邮件主题

    message = MIMEText(mail_body, 'plain', 'utf-8')  # 内容, 格式, 编码
    message['From'] = "{}".format(sender)
    message['To'] = ",".join(receivers)
    message['Subject'] = title

    try:
        smtp_object = smtplib.SMTP_SSL(mail_host, 465)  # 启用SSL发信, 端口一般是465
        smtp_object.login(mail_user, mail_pass)  # 登录验证
        smtp_object.sendmail(sender, receivers, message.as_string())  # 发送
        print("mail has been send successfully.")
    except smtplib.SMTPException as e:
        print(e)