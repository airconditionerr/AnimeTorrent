import re
import requests
from bs4 import BeautifulSoup
import configparser
import mysql.connector
from datetime import datetime

'''
    0.读取配置文件
'''
conf = configparser.ConfigParser()
conf.read('config.ini', encoding='utf-8')

# GLOBAL
# teams_excluded = conf.get('GLOBAL', 'teams_excluded').split(',')
url = conf.get('GLOBAL', 'url')
translation_groups = conf.get('GLOBAL', 'translation_groups')

# DATABASE
host = conf.get('DATABASE', 'host')
user = conf.get('DATABASE', 'username')
passwd = conf.get('DATABASE', 'password')

'''
    1.连接数据库
'''
mydb = mysql.connector.connect(host=host, user=user, passwd=passwd, database='anime_links')

'''
    2.爬取并分析目标页面
'''
response = requests.get(url)
html_doc = response.text
soup = BeautifulSoup(html_doc, 'html.parser')
tables = soup.find_all('table', class_='table table-striped tbl-border fadeIn')
anime_name_cn = soup.find('p', class_='bangumi-title').text  # 动漫中文名
translation_groups = soup.find_all('li', class_='leftbar-item')  # 翻译组们

'''
    3.获取所有磁力链接
    4.筛选出需要的磁力链接
    5.以文件形式/数据库保存磁力链接
'''


def save_torrents(mycursor, anime_name_cn, anime_episode, anime_translation_group, anime_torrent_link,
                  torrent_save_time):
    for table in tables:
        titles = table.find_all('a', class_='magnet-link-wrap')
        magnets = table.find_all('a', class_='js-magnet magnet-link')
        if re.search(translation_groups, titles[0].text) != None:
            if titles[0].text.find(translation_groups) != -1:
                for i in range(len(titles)):
                    mycursor = mydb.cursor()

                    sql = "INSERT INTO anime_torrents (anime_name_cn, anime_episode,anime_translation_group, anime_torrent_link, torrent_save_time) VALUES (%s,%s,%s,%s,%s)"
                    val = (
                        anime_name_cn, i + 1, translation_groups, magnets[i - 1].get('data-clipboard-text'),
                        datetime.now())
                    mycursor.execute(sql, val)

                    mydb.commit()  # 数据表内容有更新，必须使用到该语句

                    print(mycursor.rowcount, "记录插入成功。")
        else:
            continue
