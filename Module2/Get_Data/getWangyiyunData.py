# 获取网易云歌单信息
# 目标网站：https://music.163.com/#/discover/playlist/?order=hot&cat=%E5%85%A8%E9%83%A8&limit=35&offset=0

import requests
import re
import psycopg2
import json

class getWangyiyunData:
    def __init__(self):
        self.url="https://music.163.com/discover/playlist/?order=hot&cat=%E5%85%A8%E9%83%A8&limit=35&offset={}"
        self.headers={
            #'cookie':'_ntes_nuid=2e17fc85ed59e264236c986d7c7b9669; NMTID=00OqxadEbEAAas65EnYiEKSf6o-Qc0AAAF8zyuXpw; WEVNSM=1.0.0; WNMCID=ulxewv.1635563313052.01.0; WM_TID=w4oEgJakfxtBEQRFFFJ%2Fk5aFpHBQGLia; nts_mail_user=18211911159@163.com:-1:1; _iuqxldmzr_=32; sDeviceId=YD-9iGk0gRaFdNEAwUQRFbVzb%2BPQ5q6FD1t; NTES_P_UTID=7JHzSopaEl8zXjKtWkbXKS2e8MmCs1YU|1713204131; P_INFO=m18211911159@163.com|1713204131|0|mail163|00&99|hen&1713175274&mbmail_android#RU&null#10#0#0|182159&1|mailmaster_win&mbmail_android|18211911159@163.com; _ntes_nnid=2e17fc85ed59e264236c986d7c7b9669,1727640666541; ntes_utid=tid._.KwlcDHjluDNFBhBVEAbTXB7%252BedWbJseE._.0; __snaker__id=vdy9auUgCwOD6BP9; gdxidpyhxdE=nv7vem56TZLfjgQL4ifudVwhW3w7hpZZXDVJ%2BAZge91iw4G0SNWaCl3Yx407qiTDLZ%2BSfLK8l7TPRI2gUuiMwij00OepfUY3L0wqybmxgWnaYNjzmTs3bWURrOd9Vf1TmbgxiobTfn3yk1bzN%5CfXlZGuuPoVRkftNeAPqikOYpxOIzm%2F%3A1727642092227; WM_NI=P2WEuJcydf3Qyw%2BhXlT2f%2FboPJRDQC5qY%2Frq8uYR1rFiYZpzN1bseuMZmCxoO90nJR7QE62yTzv%2FtySgtJe07qTEeJ5DDk34hGMbSup8Sl%2BfhpDt2896fx7jhIMhz764b0w%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6eed4b67db09c818ce65af8868bb6d84e879b8fadc6609c8baa8ab346f7e8acd7b42af0fea7c3b92a94ee99a6f842a1a7ac87b25bbba9e589db6898eeaad0e16594969ea5d449f7af97d0f17bfcab97b3b47a86b797bbf3728eefae94e87f8f86a3a4fb658de7008fc95af58f8bd7b17398a6bad0f77391b9bcabe83cf5af9ca6e842f79c8c8cb240ac998383d27fb4e89d8daa6eacb08c95b134fbeaaa99b662ac978389f93df6ecaed1f637e2a3; JSESSIONID-WYYY=zAYkdTtQ2tUTFm7Dp6vO0O%2BRPX1wV%2BCSEYIQ8x7j362CmRokBRizvER1cmAfmBjHhTRk6DpQANe4OadZFzBzPnkBdMec%5CFDNkyhZjngFF%2B1inxBFfe3CM5SZG4%2B9f18oH%5CTq4afHKTcC7F3uwTfUwJnsRyRmyhF4sRSE15yZhv%2FqM2Qw%3A1727721117977',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
        }
        self.firstUrl="https://music.163.com{}"

    # 获取其中一个歌单分类页面内容（返回值类型：字符串）
    def getOnePageData(self,page):
        offset=(int(page)-1)*35
        response=requests.get(url=self.url.format(str(offset)),headers=self.headers)
        return response.content.decode()

    # 获取页面总数量（返回值类型：字符串）
    def getPagesCount(self):
        data=self.getOnePageData(page=1)
        list=re.findall(r'<a href=".*?" class="zpgi">(.*?)</a>',data)
        result=list[len(list)-1]
        return result

    # 获取所有歌单链接，所有页（返回值类型：一维列表）
    def getMusicLink(self):
        musicLinkList=[]
        for page in range(1,int(self.getPagesCount())+1):
            data=self.getOnePageData(page=page)
            list=re.findall(r'<a title=".*?" href="(.*?)" class="tit f-thide s-fc0">.*?</a>',data)
            for item in list:
                musicLinkList.append(item)
            print(page)
        return musicLinkList

    # 获取每个歌单详情页面所需要的信息（返回值类型：json）
    # 包含数据整理
    def getMusicInfo(self,lastUrl):
        data=requests.get(url=self.firstUrl.format(lastUrl),headers=self.headers).content.decode()
        # 歌单名称（类型：string）
        try:
            name=re.findall(r'<h2 class="f-ff2 f-brk">(.*?)</h2>',data)[0]
        except:
            name='NULL'
            pass
        # 歌单创建者（类型：string）
        try:
            founder=re.findall(r'<a href=".*?" class="s-fc7">(.*?)</a>',data)[0]
        except:
            founder='NULL'
            pass
        # 歌单创建日期（类型：string; 格式：yyyy-mm-dd）
        try:
            stringCD=re.findall(r'<span class="time s-fc4">(.*?)</span>',data)[0]
            creation_date=stringCD[:10]
        except:
            creation_date='NULL'
            pass
        # 歌单中的歌曲数量（类型：int）
        try:
            stringMC=re.findall(r'<span id="playlist-track-count">(.*?)</span>',data)[0]
            music_count=int(stringMC)
        except:
            music_count=-1
            pass
        # 总播放次数（类型：int）
        try:
            stringPC=re.findall(r'<strong id="play-count" class="s-fc6">(.*?)</strong>',data)[0]
            play_count=int(stringPC)
        except:
            play_count=-1
            pass
        # 收藏数量（类型：int）
        try:
            stringSC=re.findall(r'class="u-btni u-btni-fav " href="javascript:;">\n<i>(.*?)</i>',data)[0]
            save_count=int(stringSC.strip("()"))
        except:
            save_count=-1
            pass
        # 转发数量（类型：int）
        try:
            stringRC=re.findall(r'class="u-btni u-btni-share " href="javascript:;"><i>(.*?)</i></a>',data)[0]
            if(stringRC=='分享'):
                stringRC='(0)'
            reprint_count=int(stringRC.strip("()"))
        except:
            reprint_count=-1
            pass
        # 评论数量（类型：int）
        try:
            stringCC=re.findall(r'<a data-res-action="comment" href="javascript:;" class="u-btni u-btni-cmmt ">.*?<span id="cnt_comment_count">(.*?)</span>',data)[0]
            if(stringCC=='评论'):
                stringCC='0'
            commentaries_count=int(stringCC)
        except:
            commentaries_count=-1
            pass
        # 歌单标签（类型：string; 格式：list）
        try:
            tab=re.findall(r'<a class="u-tag" href=".*?"><i>(.*?)</i></a>',data)
        except:
            tab=['NULL']
            pass
        # 组合成json
        jsonData = {
            'name':name,
            'founder':founder,
            'creation_date':creation_date,
            'music_count':music_count,
            'play_count':play_count,
            'save_count':save_count,
            'reprint_count':reprint_count,
            'commentaries_count':commentaries_count,
            'tab':tab
        }
        return json.dumps(jsonData)

    # 主函数
    def main(self):
        musicLinkList=self.getMusicLink()
        # 连接到 PostgreSQL
        connectDB = psycopg2.connect(
            database="Course:Big_Data",
            user="postgres",
            password="123456",
            host="localhost",
            port="5432"
        )
        cursor=connectDB.cursor() # 游标
        # 获取每个歌单详情页面，并写入数据库
        for lastUrl in musicLinkList:
            jsonString=self.getMusicInfo(lastUrl=lastUrl)
            print(jsonString)
            try:
                insertSql="INSERT INTO music_info_json_table (music_info_json) VALUES (%s)" # SQL 语句
                cursor.execute(insertSql,(jsonString,)) # 执行 SQL 语句
                connectDB.commit() # 提交（保存）
                print("写入成功！")
            except Exception as error:
                print("写入失败！报错：{}".format(error))
                pass
        # 关闭数据库连接
        cursor.close()
        connectDB.close()


if __name__ == '__main__':
    getWangyiyunData=getWangyiyunData()
    # 该数据已收集完毕，防止重复操作！！！
    # getWangyiyunData.main()