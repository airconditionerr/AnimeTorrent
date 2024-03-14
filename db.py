import mysql.connector
def connect_mysql(conf):
    host = conf.get('DATABASE', 'host')
    user = conf.get('DATABASE', 'username')
    passwd = conf.get('DATABASE','password')
    return mysql.connector.connect(host=host, user=user, passwd=passwd, database='anime_links')

def save_anime_torrents(mydb, **var_args_dict):
    mycursor = mydb.cursor()

    sql = "INSERT INTO anime_torrents (anime_name_cn, anime_episode, anime_translation_group, anime_torrent_link, torrent_save_time, anime_description) VALUES (%s,%s,%s,%s,%s,%s)"
    val = (
        var_args_dict['anime_name_cn'],
        var_args_dict['anime_episode'],
        var_args_dict['anime_translation_group'],
        var_args_dict['anime_torrent_link'],
        var_args_dict['torrent_save_time'],
        var_args_dict['anime_description'])
    mycursor.execute(sql, val)

    mydb.commit()  # 数据表内容有更新，必须使用到该语句

    print(mycursor.rowcount, "记录插入成功。")

def anime_torrents_is_exist(mydb, **var_args_dict):
    mycursor = mydb.cursor()

    sql = "SELECT * FROM anime_torrents where anime_name_cn = %s and anime_episode = %s and anime_translation_group = %s"
    val = (
        var_args_dict['anime_name_cn'],
        var_args_dict['anime_episode'],
        var_args_dict['anime_translation_group'],)

    mycursor.execute(sql, val)
    results = mycursor.fetchall()
    if results is None or len(results) == 0:
        return True
    else:
        return False