#!/usr/bin/python3
#-*- coding: UTF-8 -*-

import pymysql.cursors

db = pymysql.connect(
        host="localhost", 
        user="root", 
        password="yxd1990", 
        db="ChineseArchive",
        charset='utf8',
        cursorclass=pymysql.cursors.DictCursor)

cursor = db.cursor()
sql = "UPDATE tag_tbl SET tag_num = 30131 WHERE tag_id=1"
cursor.execute(sql)
db.commit()

sql = "SELECT tag_num FROM tag_tbl WHERE tag_id=1"
cursor.execute(sql)
data = cursor.fetchone()

print("tag_num : %s" % data)

db.close()
