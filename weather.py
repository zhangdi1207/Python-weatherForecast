#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import datetime
import re
 
 
def get_content(url, data=None,encode='utf-8'):
    rep = requests.get(url, timeout=60)
    rep.encoding = encode
    return rep.text
 
 
def get_data(htmltext, city):
    content = []
    bs = BeautifulSoup(htmltext, "html.parser")
    body = bs.body
    data = body.find('div', {'id': '7d'})
    ul = data.find('ul')
    li = ul.find_all('li')
    for day in li:
        line = [city]
        date = day.find('h1').string
        line.append(date)
        text = day.find_all('p')
        line.append(text[0].string)
        if text[1].find('span') is None:
            temperature_H = None
        else:
            temperature_H = text[1].find('span').string.replace('℃', '')
        temperature_L = text[1].find('i').string.replace('℃', '')
        line.append(temperature_H)
        line.append(temperature_L)
        line.append(day.find(attrs={'class','win'}).find('i').string)
        for j in day.find(attrs={'class','win'}).find_all('span'):
            line.append(j.attrs['title'])

        content.append(line)
    #print(content)
    return content
 
 
def save_data(data, filename):
    with open(filename, 'w', errors='ignore', newline='') as f:
        data=str(data)
        f.write(data)
 
def landWeather():
    html = get_content("http://www.weather.com.cn/weather/101120505.shtml")
    city="longkou"
    result = get_data(html, city)
    return result

def seaData(html):
    seaW=[]
    tempD=[]

    windDict={'东风':'east wind','东北风':'northeast wind','北风':'north wind','西北风':'northwest wind',
    '西风':'west wind','西南风':'southwest wind','南风':'south wind','东南风':'southeast wind'}
    windList=windDict.keys()
    html = BeautifulSoup(html, "html.parser").body
    html = html.find(text="山东海洋天气预报").parent.parent.parent.parent.parent.find(text='海洋天气预报：').parent.parent.parent
    text=html.get_text()
    p1=r"[。|\n][^。]*?渤海[^。]*?\d级[^。]*?。"
    pattern1=re.compile(p1)
    text=pattern1.findall(text)
    if len(text)==3:
        for i in range(len(text)):
            windSer=1
            for wind in windList:
                if wind in text[i]:
                    pass


    #print(text)
    return str(html.get_text)
def seaWeather():
    html = get_content("http://www.sdqx.gov.cn/sdqx_hyyb.asp",encode="gbk")
    
    return seaData(html)


def mailData(landData,seaData):
    weekList=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    weekListC=['星期一','星期二','星期三','星期四','星期五','星期六','星期天']
    weatherDict={"阴":"overcast",'晴':'clear','雷阵雨':'thunder shower',
    '多云':'cloudy','多云':'cloudy','阵雨':'shower','小雨':'light rain','小到中雨':'light to moderate rain','雨夹雪':'sleet','小雪':'light snow','中雪':'moderate snow','大雪':'heavy snow'}
    windDict={'东风':'east wind','东北风':'northeast wind','北风':'north wind','西北风':'northwest wind',
    '西风':'west wind','西南风':'southwest wind','南风':'south wind','东南风':'southeast wind'}
    with open('model.html',encoding='UTF-8') as f:
        t=f.read()
        nowDate=datetime.datetime.now()
        t=t.replace('myDataSea',seaData)
        t=t.replace('myData0000',str(nowDate.date()))
        t=t.replace('myData0100',str(nowDate.date()+datetime.timedelta(days=2)))
        for ser,mydate in enumerate(['01','02','03']):
            nowDate=datetime.datetime.now()+datetime.timedelta(days=ser)
            t=t.replace('myData01'+mydate,str(nowDate.date()))
            t=t.replace('myData02'+mydate,landData[ser][3])
            t=t.replace('myData03'+mydate,weekListC[nowDate.weekday()])
            t=t.replace('myData04'+mydate,landData[ser][2])
            temp=landData[ser][6]
            if landData[ser][6]!=landData[ser][7]:
                temp+='转'+landData[ser][7]
            t=t.replace('myData05'+mydate,temp)
            temp=str(landData[ser][5])
            t=t.replace('myData06'+mydate,temp)
            ############
            
            t=t.replace('myData08'+mydate,weekList[nowDate.weekday()])
            t=t.replace('myData09'+mydate,landData[ser][4])
            ################
            temp=''
            if '转' in landData[ser][2]:
                for tempw in landData[ser][2].split('转'):
                    temp+= weatherDict[tempw]+' to '
                temp=temp[:-3]
            else:
                temp=weatherDict[landData[ser][2]]
            t=t.replace('myData10'+mydate,temp)


            ################
            temp=''
            if landData[ser][6]!=landData[ser][7]:
                temp += windDict[landData[ser][6]] + ' to ' + windDict[landData[ser][7]]
            else:
                temp=windDict[landData[ser][6]]
            t=t.replace('myData11'+mydate,temp)
            #
            #
            temp='wind grade '
            if '转' in landData[ser][5]:
                for tempw in landData[ser][5].split('转'):
                    temp+= tempw.replace('级','') + ' to '
                temp=temp[:-4]
            else:
                temp+=landData[ser][5].replace('级','')
            t=t.replace('myData12'+mydate,temp)

        out = open('1.html','w',encoding='utf-8')
        out.write(t)
        out.close()
    


 
if __name__ == '__main__':
    landData = landWeather()[:3]
    seaData = seaWeather()
    #landData.append(seaData)
    #print(seaData)
    mailData(landData,seaData)
