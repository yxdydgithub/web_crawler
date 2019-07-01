#!/usr/bin/env python
# coding: utf-8

# In[24]:


import time
import random
import requests
import datetime
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from lxml import etree
import os
import pandas as pd
import pymysql.cursors


# In[25]:


def get_FileSize(filePath):
    fsize = os.path.getsize(filePath)
    fsize = fsize/float(1024)
    print(int(fsize))
    return int(fsize)


# In[26]:


def get(url,i):
    print('获取第%s页' %i)
    driver.get(url)
    time.sleep(15)
    list = driver.page_source
    print('保存第%s页' %i)
    file=open('/home/yxd/Documents/webcrawler/archive_data/%s.txt'%i,'w+',encoding='utf-8')
    file.write(list)
    file.close()
    updatePageNumFromDB()


# In[27]:


def connDB():
    db = pymysql.connect(
            host = "localhost",
            user = "root",
            passwd = "yxd1990",
            db = "ChineseArchive",
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor)
    return db


# In[28]:


def getPageNumFromDB():
    db = connDB()    
    cursor = db.cursor()
    try:
        cursor.execute("SELECT tag_num FROM tag_tbl WHERE tag_id=1")
        pageNum = cursor.fetchone()
        db.commit()
    except:
        db.roolback()
    db.close()
    return pageNum


# In[29]:


def updatePageNumFromDB():
    db = connDB()
    cursor = db.cursor()
    sql = "UPDATE tag_tbl SET tag_num=tag_num+1 WHERE tag_id=1"
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
    db.close()


# In[30]:


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--disable-infobars')
chrome_options.add_argument('--start-maximized')
# chrome_options.add_argument('--user-data-dir=C:\\Users\cc\AppData\Local\Google\Chrome\\User Data')
driver = webdriver.Chrome(chrome_options=chrome_options)


# In[31]:


pageNum = getPageNumFromDB()
pageNum = pageNum['tag_num']

# In[ ]:

for i in range (pageNum, 63448):
    
    url = "http://www.lsdag.com/COMMON/ajax/Ajax.ashx?obj=Lsda&type=LsdaSearch&curr=%s&numPerPage=20&title=&sn=&guanzhi=&zerenzhe=&yuanjinian=&_=1542642296731" %i
    get(url,i) 
    s1 = '/home/yxd/Documents/webcrawler/archive_data/'
    s2 =  ".txt"
    path = s1 + str(i) + s2
    fileSize = get_FileSize(path)
    if fileSize < 3:
        driver.close()
        time.sleep(20)
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--disable-infobars')
        chrome_options.add_argument('--start-maximized')
        # chrome_options.add_argument('--user-data-dir=C:\\Users\cc\AppData\Local\Google\Chrome\\User Data')
        driver = webdriver.Chrome(chrome_options=chrome_options)
        get(url,i)
    else:
        continue 
    print("upodate i values: %s" % i)


