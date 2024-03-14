create table if not exists anime_torrents
(
    id                      int unsigned auto_increment comment '自增id'
        primary key,
    anime_name_cn           varchar(100) not null comment '中文番名',
    anime_name_jp           varchar(100) null comment '日语番名',
    anime_episode           varchar(10)  not null comment '集数',
    anime_translation_group varchar(20)  not null comment '翻译组',
    anime_torrent_link      text         not null comment '磁力链接',
    torrent_save_time       datetime     not null comment '磁力链接保存时间',
    anime_description       text         null comment '描述'
);

