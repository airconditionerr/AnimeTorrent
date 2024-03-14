import re
import requests
from bs4 import BeautifulSoup
import configparser
import db
from datetime import datetime

'''
    0.读取配置文件
'''
conf = configparser.ConfigParser()
conf.read('config.ini', encoding='utf-8')

# GLOBAL
url = conf.get('GLOBAL', 'url')
translation_groups_needed = conf.get('GLOBAL', 'translation_groups_needed')

# 1.连接数据库
mydb = db.connect_mysql(conf)

'''
    2.爬取并分析目标页面
'''
response = requests.get(url)
html_doc = response.text
soup = BeautifulSoup(html_doc, 'html.parser')
tables = soup.find_all('table', class_='table table-striped tbl-border fadeIn')
anime_name_cn = soup.find('p', class_='bangumi-title').text  # 动漫中文名
translation_groups = soup.find_all('a', class_='subgroup-name')  # 翻译组们
'''
    3.获取所有磁力链接
    4.筛选出需要的磁力链接
    5.以文件形式/数据库保存磁力链接
'''
groups_num = 0
for table in tables:
    titles = table.find_all('a', class_='magnet-link-wrap')
    magnets = table.find_all('a', class_='js-magnet magnet-link')
    print(groups_num, translation_groups[groups_num].text)
    for i in range(len(titles)):
        if db.anime_torrents_is_exist(mydb,
                                      anime_name_cn=anime_name_cn,
                                      anime_episode=i + 1,
                                      anime_translation_group=translation_groups[groups_num].text):
            db.save_anime_torrents(mydb,
                                   anime_name_cn=anime_name_cn,
                                   anime_episode=i + 1,
                                   anime_translation_group=translation_groups[groups_num].text,
                                   anime_torrent_link=magnets[i - 1].get('data-clipboard-text'),
                                   torrent_save_time=datetime.now(),
                                   anime_description=titles[i].text)
        else:
            continue
    groups_num = groups_num + 1
