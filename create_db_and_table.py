## db 와 테이블 만들기

from database import config
import mysql.connector


db = mysql.connector.connect(**config)
cursor = db.cursor()

cursor.execute(
    """
    create database if not exists news_recommend default character set 'utf8';
    """
)


cursor.execute(
    """
    drop table if exists news_recommend.news_ago;
    """
)

cursor.execute(
    """
    create table if not exists news_recommend.news_ago(
    gid varchar(10) primary key,
    createtime timestamp,
    title varchar(100),
    content mediumblob,
    url varchar(100),
    thumburl varchar(100),
    source varchar(10),
    length int,
    vec mediumblob,
    konlpy mediumblob
    );
    """
)
