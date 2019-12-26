import urllib.request
from bs4 import BeautifulSoup
import requests
import random
import time
import json
from mssql import MSSQL
import io
import sys

from mssql import MSSQL

USER_AGENTS = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
]


def openUrl(url):
    # 构造 Request headers
    agent = random.choice(USER_AGENTS)
    headers = {
        "Host": "item.jd.com",
        "Referer": "",
        #"Accept-Encoding":"gzip, deflate, br",
        'User-Agent': agent
    }
    
    #urllib.request库用来向该网服务器发送请求，请求打开该网址链接
    html = requests.get(url, headers=headers)       
    #BeautifulSoup库解析获得的网页，第二个参数一定记住要写上"html.parser"，记住就行
    bsObj = BeautifulSoup(html.content, "html.parser")
    return bsObj

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8') #改变标准输出的默认编码

ms = MSSQL(host="10.252.36.77",user="sa",pwd="888888",db="Welfare")
cnt = ms.ExecQuery("select count(sku) as cnt from Products where UpdateTime is null")

for row in range(1,int(cnt[0][0])):
    try:
        selsql="select * from(SELECT ROW_NUMBER() over (order by sku) as rownum, sku FROM Products where UpdateTime is null) as t1 where rownum="+str(row)
        res = ms.ExecQuery(selsql)
        sku = res[0][1]
        url = 'https://item.jd.com/'+ sku +'.html'
        result=openUrl(url)
        crumb = result.find("div", {"class":{"crumb fl clearfix"}})
        cat   = crumb.findAll("div",{"class":{"item"}})
        cat1  = cat[0].get_text()
        cat2  = cat[2].get_text()
        cat3  = cat[4].get_text()
        brank = cat[6].find("a").get_text()
        upsql="Update Products set FirstClass = '" + cat1 + "', SecondClass = '" + cat2 + "', ThirdClass = '" + cat3 + "', Brands = '" + brank.replace("'","''") + "' ,UpdateTime=getdate() where sku=" + sku
        ms.ExecNonQuery(upsql)
        print ("+"*50)
        print ("success!!!")
        time.sleep(2)
    except:
        upsql="insert into Error(ErrorId, sku,CreateTime) values(newid(), '"+sku +"', getdate())"
        ms.ExecNonQuery(upsql)
        print ("-"*50)
        print ("error!!!")
        print (str(row))
        time.sleep(40)


