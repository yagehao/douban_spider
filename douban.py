#目标网站：https://movie.douban.com/tag/#/?sort=S&range=0,10&tags=%E7%94%B5%E5%BD%B1,%E9%9F%B3%E4%B9%90%E5%89%A7&start=0
#============================================================
#准备工作
#============================================================
# -*- encoding: utf-8 -*-

#导入module
import requests
import random
import json
import time
from openpyxl import Workbook

#class实例化
wb = Workbook()
#激活工具表
ws = wb.active
#添加表头
ws.append(['title', 'rate', 'casts', 'url', 'cover'])

#============================================================
#下载网页数据
#============================================================
#设置requests请求的headers
headers = {
    'Accept': 'application/json, text/plain, */*',
    #'Accept-Encoding': 'gzip, deflate, br', #添加本字段会使response内容乱码
    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,ja;q=0.6,zh-TW;q=0.5',
    'Connection': 'keep-alive',
    'Host': 'movie.douban.com',
    'Referer': 'https://movie.douban.com/tag/',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
}

#设置动态js的url
url = 'https://movie.douban.com/j/new_search_subjects'

#获取多页数据
for start in range(0,50,10):
    #随机睡眠1-2s
    time.sleep(random.uniform(1, 2))

    #设置url post请求的参数
    params = {
        "sort":"S",
        "range":"0,10",
        "tags":"电影,音乐剧",
        "start": start
    }

    #requests get请求下载
    response = requests.get(url, headers=headers, params=params).text
    #print(response)

#=============================================================
#解析下载内容
#=============================================================
    #获取json字符串数据
    str_json = response[8:-1]
    #把json数据转成dict类型
    data = json.loads(str_json)

#=============================================================
#存储文字信息到excel
#=============================================================
    for item in data:
        #list格式需要转化为字符串
        casts_str = ','.join(item['casts'])

        #写入excel
        ws.append([item['title'], item['rate'], casts_str, item['url'], item['cover']])
    wb.save('musicals.xlsx')

#=============================================================
#下载并储存图片到本地
#=============================================================
    for item in data:
        #print(item['cover'])

        pic = requests.get(item['cover'], timeout=7)

        string = item['title'] + '.jpg'
        fp = open(string, 'wb')

        fp.write(pic.content)
        fp.flush()
        fp.close()

#=============================================================
#Reference
#=============================================================
#https://zhuanlan.zhihu.com/p/22097627
#https://zhuanlan.zhihu.com/p/139290537
#https://blog.csdn.net/guanmaoning/article/details/80158554
#https://blog.csdn.net/weixin_43881394/article/details/106281532
#https://blog.csdn.net/roytao2/article/details/53433373
#https://blog.csdn.net/qq_39884947/article/details/86691476?utm_medium=distribute.pc_relevant.none-task-blog-BlogCommendFromMachineLearnPai2-4.nonecase&depth_1-utm_source=distribute.pc_relevant.none-task-blog-BlogCommendFromMachineLearnPai2-4.nonecase

#=============================================================
#Useful Tools
#=============================================================
#https://www.convertonline.io/convert/query-string-to-json
#http://www.json.cn/
