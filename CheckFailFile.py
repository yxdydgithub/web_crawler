#! /usr/bin/python3

#coding: 'utf-8'

import os
import time
import random
import datetime
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.proxy import Proxy
from selenium.webdriver.common.proxy import ProxyType
from selenium import webdriver
from lxml import etree
import json
import requests

def ipProxies():
    r = requests.get('http://127.0.0.1:8000/?types=0&count=10&country=国内')
    ip_ports = json.loads(r.text)
    randomIP = random.randint(1,9)
    ip = ip_ports[randomIP][0]
    port = ip_ports[randomIP][1]
    proxies = {
            'http':'%s:%s'%(ip,port)
            }
    myProxy = proxies.get('http')
    print("Now using IP: "+ str(myProxy))
    return myProxy


def get(url,i):
    print('获取第%s页' %i)
    driver.get(url)
    time.sleep(15)
    pageContent = driver.page_source
    print('保存第%s页' %i)
    file=open('/home/yxd/Documents/webcrawler/archive_data/%s.txt'%i,'w+',encoding='utf-8')
    file.write(pageContent)
    file.close()

def getFailFile(filePath):
    dirList = os.listdir(filePath)
    for i in range(0, len(dirList)):
        path = os.path.join(filePath, dirList[i])
        if os.path.isfile(path):
            fileSize = os.path.getsize(path)
            fileSize = fileSize/float(1024)
            fileSize = int(fileSize)
            pageNum = int(dirList[i].split(".")[0])
            if fileSize < 2 or fileSize > 6:
                print("fileSize: %s" %fileSize) 
                url = "http://www.lsdag.com/COMMON/ajax/Ajax.ashx?obj=Lsda&type=LsdaSearch&curr=%s&numPerPage=20&title=&sn=&guanzhi=&zerenzhe=&yuanjinian=&_=1542642296731" %pageNum
                try:
                    if i % 10 == 0:
                        driver.close()
                        chrome_options = webdriver.ChromeOptions()
                        chrome_options.add_argument('--proxy-server=%s' % ipProxies())
                        driver = webdriver.Chrome(chrome_options = chrome_options)
                    print("everything is normal!")
                    get(url,pageNum)
                except:
                    print("enter into except code!!!")
                    time.sleep(15)
                    chrome_options = webdriver.ChromeOptions()
                    chrome_options.add_argument('--disable-infobars')
                    chrome_options.add_argument('--proxy-server=%s' % ipProxies())
                    chrome_options.add_argument('--start-maximized')
                    driver = webdriver.Chrome(chrome_options = chrome_options)
                    driver.quit()
                    get(url,pageNum)
            else:
                continue
        else:
            continue
    print("Every file is successful!")

if __name__ == '__main__':
    
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--disable-infobars')
    chrome_options.add_argument('--proxy-server=%s' % ipProxies())
    chrome_options.add_argument('--start-maximized')
    driver = webdriver.Chrome(chrome_options = chrome_options)

    filePath = '/home/yxd/Documents/webcrawler/archive_data/'
    getFailFile(filePath)
