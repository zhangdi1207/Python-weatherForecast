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
    web='''
    <html dir="ltr">
    <head>
    <meta http-equiv="Content-Type" content="text/html; charset=gb2312">
    <style title="owaParaStyle"><!--P {
        MARGIN-TOP: 0px; MARGIN-BOTTOM: 0px
    }
    --></style>
    <meta name="GENERATOR" content="MSHTML 8.00.7601.18667">
    </head>
    <body ocsi="x">
    <div></div>
    <div dir="ltr"><span style="FONT-FAMILY: '微软雅黑','sans-serif'; COLOR: black">各位好<span lang="EN-US">,</span></span><span style="FONT-FAMILY: 'Tahoma','sans-serif'; COLOR: gray; FONT-SIZE: 10pt" lang="EN-US">
    </span></div>
    <div>
    <p style="MARGIN: 0cm 0cm 0pt" dir="ltr" class="MsoNormal"><span style="FONT-FAMILY: '微软雅黑','sans-serif'; COLOR: black">以下为近三天天气预报，请各部门参考。</span></p>
    <p style="MARGIN: 0cm 0cm 0pt" dir="ltr" class="MsoNormal"><span style="FONT-FAMILY: '微软雅黑','sans-serif'; COLOR: black"></span><span style="FONT-FAMILY: '微软雅黑','sans-serif'; COLOR: black"></span><span style="FONT-FAMILY: '微软雅黑','sans-serif'; COLOR: black">具体预报如下：</p>
    <p style="MARGIN: 0cm 0cm 0pt" dir="ltr" class="MsoNormal"><span style="FONT-FAMILY: '微软雅黑','sans-serif'; COLOR: black"></span><span style="FONT-FAMILY: '微软雅黑','sans-serif'; COLOR: black"></span><span style="FONT-FAMILY: '微软雅黑','sans-serif'; COLOR: black">myDataSea</p>
    <p style="MARGIN: 0cm 0cm 0pt" dir="ltr" class="MsoNormal">
    <table style="WIDTH: 842pt; BORDER-COLLAPSE: collapse" border="0" cellspacing="0" cellpadding="0" width="1120">
    <colgroup><col style="WIDTH: 64pt; mso-width-source: userset; mso-width-alt: 2720" span="2" width="85"><col style="WIDTH: 82pt; mso-width-source: userset; mso-width-alt: 3488" width="109"><col style="WIDTH: 46pt; mso-width-source: userset; mso-width-alt: 1952" width="61"><col style="WIDTH: 136pt; mso-width-source: userset; mso-width-alt: 5792" span="3" width="181"><col style="WIDTH: 178pt; mso-width-source: userset; mso-width-alt: 7584" width="237"></colgroup>
    <tbody>
    <tr style="HEIGHT: 36pt; mso-height-source: userset" height="48">
    <td style="BORDER-BOTTOM: windowtext 1pt solid; BORDER-LEFT: windowtext 1pt solid; BACKGROUND-COLOR: transparent; WIDTH: 528pt; HEIGHT: 36pt; BORDER-TOP: windowtext 1pt solid; BORDER-RIGHT: black 1pt solid" class="xl109" height="48" width="702" colspan="6">
    <p align="center"><font size="5"><strong><font face="Times New Roman">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; </font>
    <font class="font7" face="宋体">天气预报</font><font class="font6" face="Times New Roman"> Weather Forecast</font></strong></font></p>
    </td>
    <td style="BORDER-BOTTOM: windowtext 1pt solid; BORDER-LEFT: windowtext; BACKGROUND-COLOR: transparent; WIDTH: 314pt; BORDER-TOP: windowtext 1pt solid; BORDER-RIGHT: black 1pt solid" class="xl112" width="418" colspan="2">
    <p align="right"><font size="2"><strong><font face="宋体">发布周期</font><font class="font9" face="Times New Roman">:myData0000</font><font class="font8" face="宋体">至</font><font class="font9" face="Times New Roman">myData0100</font></strong></font></p>
    </td>
    </tr>
    <tr style="HEIGHT: 13.5pt; mso-height-source: userset" height="18">
    <td style="BORDER-BOTTOM: #f0f0f0; BORDER-LEFT: windowtext 1pt solid; BACKGROUND-COLOR: transparent; WIDTH: 64pt; HEIGHT: 13.5pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1pt solid" class="xl63" height="18" width="85">
    <p align="center"><font face="宋体"><strong>日期</strong></font></p>
    </td>
    <td style="BORDER-BOTTOM: #f0f0f0; BORDER-LEFT: #f0f0f0; BACKGROUND-COLOR: transparent; WIDTH: 64pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1pt solid" class="xl65" width="85">
    <p align="center"><font face="宋体"><strong>昼夜</strong></font></p>
    </td>
    <td style="BORDER-BOTTOM: #f0f0f0; BORDER-LEFT: windowtext; BACKGROUND-COLOR: transparent; WIDTH: 128pt; BORDER-TOP: windowtext 1pt solid; BORDER-RIGHT: black 1pt solid" class="xl114" width="170" colspan="2">
    <p align="center"><font face="宋体"><strong>温度</strong></font></p>
    </td>
    <td style="BORDER-BOTTOM: #f0f0f0; BORDER-LEFT: #f0f0f0; BACKGROUND-COLOR: transparent; WIDTH: 136pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1pt solid" class="xl66" width="181">
    <p align="center"><font face="宋体"><strong>天气现象</strong></font></p>
    </td>
    <td style="BORDER-BOTTOM: #f0f0f0; BORDER-LEFT: #f0f0f0; BACKGROUND-COLOR: transparent; WIDTH: 136pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1pt solid" class="xl66" width="181">
    <p align="center"><font face="宋体"><strong>风向</strong></font></p>
    </td>
    <td style="BORDER-BOTTOM: #f0f0f0; BORDER-LEFT: windowtext; BACKGROUND-COLOR: transparent; WIDTH: 314pt; BORDER-TOP: windowtext 1pt solid; BORDER-RIGHT: black 1pt solid" class="xl116" width="418" colspan="2">
    <p align="center"><font face="宋体"><strong>风力</strong></font></p>
    </td>
    </tr>
    <tr style="HEIGHT: 15pt" height="20">
    <td style="BORDER-BOTTOM: #f0f0f0; BORDER-LEFT: windowtext 1pt solid; BACKGROUND-COLOR: transparent; WIDTH: 64pt; HEIGHT: 15pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1pt solid" class="xl64" height="20" width="85">
    <p align="center"><strong><font face="Times New Roman">Date</font></strong></p>
    </td>
    <td style="BORDER-BOTTOM: #f0f0f0; BORDER-LEFT: #f0f0f0; BACKGROUND-COLOR: transparent; WIDTH: 64pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1pt solid" class="xl89" width="85">
    <p align="center"><strong><font face="Times New Roman">Day/Night<span style="mso-spacerun: yes">&nbsp;</span></font></strong></p>
    </td>
    <td style="BORDER-BOTTOM: #f0f0f0; BORDER-LEFT: windowtext; BACKGROUND-COLOR: transparent; WIDTH: 128pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: black 1pt solid" class="xl118" width="170" colspan="2">
    <p align="center"><strong><font face="Times New Roman">Temperature</font></strong></p>
    </td>
    <td style="BORDER-BOTTOM: #f0f0f0; BORDER-LEFT: #f0f0f0; BACKGROUND-COLOR: transparent; WIDTH: 136pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1pt solid" class="xl67" width="181">
    <p align="center"><strong><font face="Times New Roman">Weather</font></strong></p>
    </td>
    <td style="BORDER-BOTTOM: #f0f0f0; BORDER-LEFT: #f0f0f0; BACKGROUND-COLOR: transparent; WIDTH: 136pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1pt solid" class="xl67" width="181">
    <p align="center"><strong><font face="Times New Roman">Wind Direction</font></strong></p>
    </td>
    <td style="BORDER-BOTTOM: windowtext 1pt solid; BORDER-LEFT: windowtext; BACKGROUND-COLOR: transparent; WIDTH: 314pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: black 1pt solid" class="xl119" width="418" colspan="2">
    <p align="center"><strong><font face="Times New Roman">Wind Power</font></strong></p>
    </td>
    </tr>
    <tr style="HEIGHT: 13.5pt" height="18">
    <td style="BORDER-BOTTOM: #f0f0f0; BORDER-LEFT: windowtext 1pt solid; BACKGROUND-COLOR: transparent; WIDTH: 64pt; HEIGHT: 13.5pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1pt solid" class="xl84" height="18" width="85">
    <p align="center"><font face="宋体">　</font></p>
    </td>
    <td style="BORDER-BOTTOM: #f0f0f0; BORDER-LEFT: #f0f0f0; BACKGROUND-COLOR: transparent; WIDTH: 64pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1pt solid" class="xl87" width="85">
    <p align="center"><font face="宋体">　</font></p>
    </td>
    <td style="BORDER-BOTTOM: #f0f0f0; BORDER-LEFT: windowtext; BACKGROUND-COLOR: transparent; WIDTH: 128pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: black 1pt solid" class="xl107" width="170" colspan="2">
    <p align="center"><font face="宋体">　</font></p>
    </td>
    <td style="BORDER-BOTTOM: #f0f0f0; BORDER-LEFT: #f0f0f0; BACKGROUND-COLOR: transparent; WIDTH: 136pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1pt solid" class="xl87" width="181">
    <p align="center"><font face="宋体">　</font></p>
    </td>
    <td style="BORDER-BOTTOM: #f0f0f0; BORDER-LEFT: #f0f0f0; BACKGROUND-COLOR: transparent; WIDTH: 136pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1pt solid" class="xl87" width="181">
    <p align="center"><font face="宋体">　</font></p>
    </td>
    <td style="BORDER-BOTTOM: #f0f0f0; BORDER-LEFT: #f0f0f0; BACKGROUND-COLOR: transparent; WIDTH: 136pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1pt solid" class="xl66" width="181">
    <p align="center"><strong><font face="宋体">沿海及内陆</font></strong></p>
    </td>
    <td style="BORDER-BOTTOM: #f0f0f0; BORDER-LEFT: #f0f0f0; BACKGROUND-COLOR: transparent; WIDTH: 178pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1pt solid" class="xl66" width="237">
    <p align="center"><strong><font face="宋体">海面</font></strong></p>
    </td>
    </tr>
    <tr style="HEIGHT: 15pt" height="20">
    <td style="BORDER-BOTTOM: windowtext 1pt solid; BORDER-LEFT: windowtext 1pt solid; BACKGROUND-COLOR: transparent; WIDTH: 64pt; HEIGHT: 15pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1pt solid" class="xl85" height="20" width="85">
    <p align="center"><font face="宋体">　</font></p>
    </td>
    <td style="BORDER-BOTTOM: windowtext 1pt solid; BORDER-LEFT: #f0f0f0; BACKGROUND-COLOR: transparent; WIDTH: 64pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1pt solid" class="xl88" width="85">
    <p align="center"><font face="宋体">　</font></p>
    </td>
    <td style="BORDER-BOTTOM: windowtext 1pt solid; BORDER-LEFT: windowtext; BACKGROUND-COLOR: transparent; WIDTH: 128pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: black 1pt solid" class="xl108" width="170" colspan="2">
    <p align="center"><font face="宋体">　</font></p>
    </td>
    <td style="BORDER-BOTTOM: windowtext 1pt solid; BORDER-LEFT: #f0f0f0; BACKGROUND-COLOR: transparent; WIDTH: 136pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1pt solid" class="xl88" width="181">
    <p align="center"><font face="宋体">　</font></p>
    </td>
    <td style="BORDER-BOTTOM: windowtext 1pt solid; BORDER-LEFT: #f0f0f0; BACKGROUND-COLOR: transparent; WIDTH: 136pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1pt solid" class="xl88" width="181">
    <p align="center"><font face="宋体">　</font></p>
    </td>
    <td style="BORDER-BOTTOM: windowtext 1pt solid; BORDER-LEFT: #f0f0f0; BACKGROUND-COLOR: transparent; WIDTH: 136pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1pt solid" class="xl68" width="181">
    <p align="center"><strong><font face="Times New Roman">Coastal and Inland</font></strong></p>
    </td>
    <td style="BORDER-BOTTOM: windowtext 1pt solid; BORDER-LEFT: #f0f0f0; BACKGROUND-COLOR: transparent; WIDTH: 178pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1pt solid" class="xl68" width="237">
    <p align="center"><strong><font face="Times New Roman">At Sea</font></strong></p>
    </td>
    </tr>
    <tr style="HEIGHT: 18pt; mso-height-source: userset" height="24">
    <td style="BORDER-BOTTOM: #f0f0f0; BORDER-LEFT: windowtext 1pt solid; BACKGROUND-COLOR: white; WIDTH: 64pt; HEIGHT: 18pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1pt solid" class="xl77" height="24" width="85">
    <p align="center"><strong><font size="2" face="Times New Roman">myData0101</font></strong></p>
    </td>
    <td style="BORDER-BOTTOM: #f0f0f0; BORDER-LEFT: #f0f0f0; BACKGROUND-COLOR: transparent; WIDTH: 64pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1pt solid" class="xl70" width="85">
    <p align="center"><font class="font11" size="2" face="宋体">白天</font></p>
    </td>
    <td style="BORDER-BOTTOM: #f0f0f0; BORDER-LEFT: #f0f0f0; BACKGROUND-COLOR: transparent; WIDTH: 82pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1pt solid" class="xl70" width="109">
    <p align="center"><font class="font11" size="2" face="宋体">高温</font></p>
    </td>
    <td style="BORDER-BOTTOM: black 1pt solid; BORDER-LEFT: windowtext 1pt solid; BACKGROUND-COLOR: transparent; WIDTH: 46pt; BORDER-TOP: windowtext; BORDER-RIGHT: windowtext 1pt solid" class="xl99" rowspan="2" width="61">
    <p align="center"><font size="2"><font face="Times New Roman">myData0201</font><font class="font11" face="宋体">℃</font></font></p>
    </td>
    <td style="BORDER-BOTTOM: #f0f0f0; BORDER-LEFT: #f0f0f0; BACKGROUND-COLOR: transparent; WIDTH: 136pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1pt solid" class="xl70" width="181">
    <p align="center"><font size="2" face="Times New Roman">　</font></p>
    </td>
    <td style="BORDER-BOTTOM: #f0f0f0; BORDER-LEFT: #f0f0f0; BACKGROUND-COLOR: white; WIDTH: 136pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1pt solid" class="xl72" width="181">
    <p align="center"><font size="2" face="Times New Roman">　</font></p>
    </td>
    <td style="BORDER-BOTTOM: #f0f0f0; BORDER-LEFT: #f0f0f0; BACKGROUND-COLOR: transparent; WIDTH: 136pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1pt solid" class="xl70" width="181">
    <p align="center"><font size="2" face="Times New Roman">　</font></p>
    </td>
    <td style="BORDER-BOTTOM: #f0f0f0; BORDER-LEFT: #f0f0f0; BACKGROUND-COLOR: transparent; WIDTH: 178pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1pt solid" class="xl70" width="237">
    <p align="center"><font size="2" face="Times New Roman">　</font></p>
    </td>
    </tr>
    <tr style="HEIGHT: 18pt; mso-height-source: userset" height="24">
    <td style="BORDER-BOTTOM: #f0f0f0; BORDER-LEFT: windowtext 1pt solid; BACKGROUND-COLOR: white; WIDTH: 64pt; HEIGHT: 18pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1pt solid" class="xl78" height="24" width="85">
    <p align="center"><strong><font size="2" face="宋体">myData0301</font></strong></p>
    </td>
    <td style="BORDER-BOTTOM: windowtext 1pt solid; BORDER-LEFT: #f0f0f0; BACKGROUND-COLOR: white; WIDTH: 64pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1pt solid" class="xl71" width="85">
    <p align="center"><font size="2" face="Times New Roman">Day</font></p>
    </td>
    <td style="BORDER-BOTTOM: windowtext 1pt solid; BORDER-LEFT: #f0f0f0; BACKGROUND-COLOR: transparent; WIDTH: 82pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1pt solid" class="xl69" width="109">
    <p align="center"><font size="2" face="Times New Roman">High temperature</font></p>
    </td>
    <td style="BORDER-BOTTOM: #f0f0f0; BORDER-LEFT: #f0f0f0; BACKGROUND-COLOR: transparent; WIDTH: 136pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1pt solid" class="xl76" width="181">
    <p align="center"><font size="2" face="宋体">myData0401</font></p>
    </td>
    <td style="BORDER-BOTTOM: #f0f0f0; BORDER-LEFT: #f0f0f0; BACKGROUND-COLOR: transparent; WIDTH: 136pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1pt solid" class="xl76" width="181">
    <p align="center"><font size="2" face="宋体">myData0501</font></p>
    </td>
    <td style="BORDER-BOTTOM: #f0f0f0; BORDER-LEFT: windowtext; BACKGROUND-COLOR: transparent; WIDTH: 136pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1pt solid" class="xl86" width="181">
    <p align="center"><font size="2"><font face="Times New Roman">myData0601</font></font></p>
    </td>
    <td style="BORDER-BOTTOM: #f0f0f0; BORDER-LEFT: windowtext; BACKGROUND-COLOR: transparent; WIDTH: 178pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1pt solid" class="xl73" width="237">
    <p align="center"><font size="2"><font face="Times New Roman">myData0701</font></font></p>
    </td>
    </tr>
    <tr style="HEIGHT: 24.75pt; mso-height-source: userset" height="33">
    <td style="BORDER-BOTTOM: #f0f0f0; BORDER-LEFT: windowtext 1pt solid; BACKGROUND-COLOR: white; WIDTH: 64pt; HEIGHT: 24.75pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1pt solid" class="xl79" height="33" width="85">
    <p align="center"><strong><font size="2" face="Times New Roman">myData0801</font></strong></p>
    </td>
    <td style="BORDER-BOTTOM: #f0f0f0; BORDER-LEFT: #f0f0f0; BACKGROUND-COLOR: white; WIDTH: 64pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1pt solid" class="xl72" width="85">
    <p align="center"><font class="font11" size="2" face="宋体">夜间</font></p>
    </td>
    <td style="BORDER-BOTTOM: #f0f0f0; BORDER-LEFT: #f0f0f0; BACKGROUND-COLOR: white; WIDTH: 82pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1pt solid" class="xl72" width="109">
    <p align="center"><font class="font11" size="2" face="宋体">低温</font></p>
    </td>
    <td style="BORDER-BOTTOM: black 1pt solid; BORDER-LEFT: windowtext 1pt solid; BACKGROUND-COLOR: transparent; WIDTH: 46pt; BORDER-TOP: windowtext; BORDER-RIGHT: windowtext 1pt solid" class="xl99" rowspan="2" width="61">
    <p align="center"><font size="2"><font face="Times New Roman">myData0901</font><font class="font11" face="宋体">℃</font></font></p>
    </td>
    <td style="BORDER-BOTTOM: #f0f0f0; BORDER-LEFT: #f0f0f0; BACKGROUND-COLOR: transparent; WIDTH: 136pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1pt solid" class="xl70" width="181">
    <p align="center"><font size="2" face="Times New Roman">myData1001</font></p>
    </td>
    <td style="BORDER-BOTTOM: #f0f0f0; BORDER-LEFT: #f0f0f0; BACKGROUND-COLOR: transparent; WIDTH: 136pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1pt solid" class="xl70" width="181">
    <p align="center"><font face="Times New Roman"><font size="2">myData1101</font></font></font></p>
    </td>
    <td style="BORDER-BOTTOM: #f0f0f0; BORDER-LEFT: windowtext; BACKGROUND-COLOR: transparent; WIDTH: 136pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1pt solid" class="xl73" width="181">
    <p align="center"><font size="2" face="Times New Roman">myData1201</font></p>
    </td>
    <td style="BORDER-BOTTOM: #f0f0f0; BORDER-LEFT: windowtext; BACKGROUND-COLOR: transparent; WIDTH: 178pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1pt solid" class="xl73" width="237">
    <p align="center"><font size="2" face="Times New Roman">myData1301</font></p>
    </td>
    </tr>
    <tr style="HEIGHT: 18pt; mso-height-source: userset" height="24">
    <td style="BORDER-BOTTOM: windowtext 1pt solid; BORDER-LEFT: windowtext 1pt solid; BACKGROUND-COLOR: white; WIDTH: 64pt; HEIGHT: 18pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1pt solid" class="xl80" height="24" width="85">
    <p align="center"><strong><font size="2" face="Times New Roman">　</font></strong></p>
    </td>
    <td style="BORDER-BOTTOM: windowtext 1pt solid; BORDER-LEFT: #f0f0f0; BACKGROUND-COLOR: white; WIDTH: 64pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1pt solid" class="xl71" width="85">
    <p align="center"><font size="2" face="Times New Roman">Night</font></p>
    </td>
    <td style="BORDER-BOTTOM: windowtext 1pt solid; BORDER-LEFT: #f0f0f0; BACKGROUND-COLOR: white; WIDTH: 82pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1pt solid" class="xl71" width="109">
    <p align="center"><font size="2" face="Times New Roman">Low temperature</font></p>
    </td>
    <td style="BORDER-BOTTOM: windowtext 1pt solid; BORDER-LEFT: #f0f0f0; BACKGROUND-COLOR: transparent; WIDTH: 136pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1pt solid" class="xl69" width="181">
    <p align="center"><font size="2" face="Times New Roman">　</font></p>
    </td>
    <td style="BORDER-BOTTOM: windowtext 1pt solid; BORDER-LEFT: #f0f0f0; BACKGROUND-COLOR: transparent; WIDTH: 136pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1pt solid" class="xl69" width="181">
    <p align="center"><font size="2" face="Times New Roman">　</font></p>
    </td>
    <td style="BORDER-BOTTOM: windowtext 1pt solid; BORDER-LEFT: #f0f0f0; BACKGROUND-COLOR: transparent; WIDTH: 136pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1pt solid" class="xl69" width="181">
    <p align="center"><font size="2" face="Times New Roman">　</font></p>
    </td>
    <td style="BORDER-BOTTOM: windowtext 1pt solid; BORDER-LEFT: #f0f0f0; BACKGROUND-COLOR: transparent; WIDTH: 178pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1pt solid" class="xl69" width="237">
    <p align="center"><font size="2" face="Times New Roman">　</font></p>
    </td>
    </tr>
    <tr style="HEIGHT: 18pt; mso-height-source: userset" height="24">
    <td style="BORDER-BOTTOM: #f0f0f0; BORDER-LEFT: windowtext 1pt solid; BACKGROUND-COLOR: white; WIDTH: 64pt; HEIGHT: 18pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1pt solid" class="xl77" height="24" width="85">
    <p align="center"><strong><font size="2" face="Times New Roman">myData0102</font></strong></p>
    </td>
    <td style="BORDER-BOTTOM: #f0f0f0; BORDER-LEFT: #f0f0f0; BACKGROUND-COLOR: white; WIDTH: 64pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1pt solid" class="xl72" width="85">
    <p align="center"><font class="font11" size="2" face="宋体">白天</font></p>
    </td>
    <td style="BORDER-BOTTOM: #f0f0f0; BORDER-LEFT: #f0f0f0; BACKGROUND-COLOR: white; WIDTH: 82pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1pt solid" class="xl72" width="109">
    <p align="center"><font class="font11" size="2" face="宋体">高温</font></p>
    </td>
    <td style="BORDER-BOTTOM: black 1pt solid; BORDER-LEFT: windowtext 1pt solid; BACKGROUND-COLOR: transparent; WIDTH: 46pt; BORDER-TOP: windowtext; BORDER-RIGHT: windowtext 1pt solid" class="xl99" rowspan="2" width="61">
    <p align="center"><font size="2"><font face="Times New Roman">myData0202</font><font class="font11" face="宋体">℃</font></font></p>
    </td>
    <td style="BORDER-BOTTOM: #f0f0f0; BORDER-LEFT: #f0f0f0; BACKGROUND-COLOR: transparent; WIDTH: 136pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1pt solid" class="xl70" width="181">
    <p align="center"><font size="2" face="Times New Roman">　</font></p>
    </td>
    <td style="BORDER-BOTTOM: #f0f0f0; BORDER-LEFT: #f0f0f0; BACKGROUND-COLOR: white; WIDTH: 136pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1pt solid" class="xl72" width="181">
    <p align="center"><font size="2" face="Times New Roman">　</font></p>
    </td>
    <td style="BORDER-BOTTOM: #f0f0f0; BORDER-LEFT: #f0f0f0; BACKGROUND-COLOR: transparent; WIDTH: 136pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1pt solid" class="xl70" width="181">
    <p align="center"><font size="2" face="Times New Roman">　</font></p>
    </td>
    <td style="BORDER-BOTTOM: #f0f0f0; BORDER-LEFT: #f0f0f0; BACKGROUND-COLOR: transparent; WIDTH: 178pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1pt solid" class="xl81" width="237">
    <p align="center"><font size="2" face="Times New Roman">　</font></p>
    </td>
    </tr>
    <tr style="HEIGHT: 18pt; mso-height-source: userset" height="24">
    <td style="BORDER-BOTTOM: #f0f0f0; BORDER-LEFT: windowtext 1pt solid; BACKGROUND-COLOR: white; WIDTH: 64pt; HEIGHT: 18pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1pt solid" class="xl78" height="24" width="85">
    <p align="center"><strong><font size="2" face="宋体">myData0302</font></strong></p>
    </td>
    <td style="BORDER-BOTTOM: windowtext 1pt solid; BORDER-LEFT: #f0f0f0; BACKGROUND-COLOR: white; WIDTH: 64pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1pt solid" class="xl71" width="85">
    <p align="center"><font size="2" face="Times New Roman">Day</font></p>
    </td>
    <td style="BORDER-BOTTOM: windowtext 1pt solid; BORDER-LEFT: #f0f0f0; BACKGROUND-COLOR: white; WIDTH: 82pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1pt solid" class="xl71" width="109">
    <p align="center"><font size="2" face="Times New Roman">High temperature</font></p>
    </td>
    <td style="BORDER-BOTTOM: #f0f0f0; BORDER-LEFT: #f0f0f0; BACKGROUND-COLOR: transparent; WIDTH: 136pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1pt solid" class="xl76" width="181">
    <p align="center"><font size="2" face="宋体">myData0402</font></p>
    </td>
    <td style="BORDER-BOTTOM: #f0f0f0; BORDER-LEFT: #f0f0f0; BACKGROUND-COLOR: transparent; WIDTH: 136pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1pt solid" class="xl76" width="181">
    <p align="center"><font size="2" face="宋体">myData0502</font></p>
    </td>
    <td style="BORDER-BOTTOM: #f0f0f0; BORDER-LEFT: windowtext; BACKGROUND-COLOR: transparent; WIDTH: 136pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1pt solid" class="xl86" width="181">
    <p align="center"><font size="2"><font face="Times New Roman">myData0602</font></font></p>
    </td>
    <td style="BORDER-BOTTOM: #f0f0f0; BORDER-LEFT: windowtext; BACKGROUND-COLOR: transparent; WIDTH: 178pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1pt solid" class="xl82" width="237">
    <p align="center"><font size="2"><font face="Times New Roman">myData0702</font></font></p>
    </td>
    </tr>
    <tr style="HEIGHT: 25.5pt; mso-height-source: userset" height="34">
    <td style="BORDER-BOTTOM: #f0f0f0; BORDER-LEFT: windowtext 1pt solid; BACKGROUND-COLOR: white; WIDTH: 64pt; HEIGHT: 25.5pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1pt solid" class="xl79" height="34" width="85">
    <p align="center"><strong><font size="2" face="Times New Roman">myData0802</font></strong></p>
    </td>
    <td style="BORDER-BOTTOM: #f0f0f0; BORDER-LEFT: #f0f0f0; BACKGROUND-COLOR: white; WIDTH: 64pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1pt solid" class="xl72" width="85">
    <p align="center"><font class="font11" size="2" face="宋体">夜间</font></p>
    </td>
    <td style="BORDER-BOTTOM: #f0f0f0; BORDER-LEFT: #f0f0f0; BACKGROUND-COLOR: white; WIDTH: 82pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1pt solid" class="xl72" width="109">
    <p align="center"><font class="font11" size="2" face="宋体">低温</font></p>
    </td>
    <td style="BORDER-BOTTOM: black 1pt solid; BORDER-LEFT: windowtext 1pt solid; BACKGROUND-COLOR: transparent; WIDTH: 46pt; BORDER-TOP: windowtext; BORDER-RIGHT: windowtext 1pt solid" class="xl99" rowspan="2" width="61">
    <p align="center"><font size="2"><font face="Times New Roman">myData0902</font><font class="font11" face="宋体">℃</font></font></p>
    </td>
    <td style="BORDER-BOTTOM: #f0f0f0; BORDER-LEFT: #f0f0f0; BACKGROUND-COLOR: transparent; WIDTH: 136pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1pt solid" class="xl70" width="181">
    <p align="center"><font size="2" face="Times New Roman">myData1002</font></p>
    </td>
    <td style="BORDER-BOTTOM: #f0f0f0; BORDER-LEFT: #f0f0f0; BACKGROUND-COLOR: transparent; WIDTH: 136pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1pt solid" class="xl70" width="181">
    <p align="center"><font size="2" face="Times New Roman">myData1102</font></p>
    </td>
    <td style="BORDER-BOTTOM: #f0f0f0; BORDER-LEFT: windowtext; BACKGROUND-COLOR: transparent; WIDTH: 136pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1pt solid" class="xl73" width="181">
    <p align="center"><font size="2" face="Times New Roman">myData1202</font></p>
    </td>
    <td style="BORDER-BOTTOM: #f0f0f0; BORDER-LEFT: windowtext; BACKGROUND-COLOR: transparent; WIDTH: 178pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1pt solid" class="xl82" width="237">
    <p align="center"><font size="2" face="Times New Roman">myData1302</font></p>
    </td>
    </tr>
    <tr style="HEIGHT: 18pt; mso-height-source: userset" height="24">
    <td style="BORDER-BOTTOM: windowtext 1pt solid; BORDER-LEFT: windowtext 1pt solid; BACKGROUND-COLOR: white; WIDTH: 64pt; HEIGHT: 18pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1pt solid" class="xl80" height="24" width="85">
    <p align="center"><strong><font size="2" face="Times New Roman">　</font></strong></p>
    </td>
    <td style="BORDER-BOTTOM: windowtext 1pt solid; BORDER-LEFT: #f0f0f0; BACKGROUND-COLOR: white; WIDTH: 64pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1pt solid" class="xl71" width="85">
    <p align="center"><font size="2" face="Times New Roman">Night</font></p>
    </td>
    <td style="BORDER-BOTTOM: windowtext 1pt solid; BORDER-LEFT: #f0f0f0; BACKGROUND-COLOR: white; WIDTH: 82pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1pt solid" class="xl71" width="109">
    <p align="center"><font size="2" face="Times New Roman">Low temperature</font></p>
    </td>
    <td style="BORDER-BOTTOM: windowtext 1pt solid; BORDER-LEFT: #f0f0f0; BACKGROUND-COLOR: transparent; WIDTH: 136pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1pt solid" class="xl69" width="181">
    <p align="center"><font size="2" face="Times New Roman">　</font></p>
    </td>
    <td style="BORDER-BOTTOM: windowtext 1pt solid; BORDER-LEFT: #f0f0f0; BACKGROUND-COLOR: transparent; WIDTH: 136pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1pt solid" class="xl69" width="181">
    <p align="center"><font size="2" face="Times New Roman">　</font></p>
    </td>
    <td style="BORDER-BOTTOM: windowtext 1pt solid; BORDER-LEFT: #f0f0f0; BACKGROUND-COLOR: transparent; WIDTH: 136pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1pt solid" class="xl69" width="181">
    <p align="center"><font size="2" face="Times New Roman">　</font></p>
    </td>
    <td style="BORDER-BOTTOM: windowtext 1pt solid; BORDER-LEFT: #f0f0f0; BACKGROUND-COLOR: transparent; WIDTH: 178pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1pt solid" class="xl83" width="237">
    <p align="center"><font size="2" face="Times New Roman">　</font></p>
    </td>
    </tr>
    <tr style="HEIGHT: 18pt; mso-height-source: userset" height="24">
    <td style="BORDER-BOTTOM: #f0f0f0; BORDER-LEFT: windowtext 1pt solid; BACKGROUND-COLOR: white; WIDTH: 64pt; HEIGHT: 18pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1pt solid" class="xl77" height="24" width="85">
    <p align="center"><strong><font size="2" face="Times New Roman">myData0103</font></strong></p>
    </td>
    <td style="BORDER-BOTTOM: #f0f0f0; BORDER-LEFT: #f0f0f0; BACKGROUND-COLOR: white; WIDTH: 64pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1pt solid" class="xl72" width="85">
    <p align="center"><font class="font11" size="2" face="宋体">白天</font></p>
    </td>
    <td style="BORDER-BOTTOM: #f0f0f0; BORDER-LEFT: #f0f0f0; BACKGROUND-COLOR: white; WIDTH: 82pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1pt solid" class="xl72" width="109">
    <p align="center"><font class="font11" size="2" face="宋体">高温</font></p>
    </td>
    <td style="BORDER-BOTTOM: black 1pt solid; BORDER-LEFT: windowtext 1pt solid; BACKGROUND-COLOR: transparent; WIDTH: 46pt; BORDER-TOP: windowtext; BORDER-RIGHT: windowtext 1pt solid" class="xl99" rowspan="2" width="61">
    <p align="center"><font size="2"><font face="Times New Roman">myData0203</font><font class="font11" face="宋体">℃</font></font></p>
    </td>
    <td style="BORDER-BOTTOM: #f0f0f0; BORDER-LEFT: #f0f0f0; BACKGROUND-COLOR: transparent; WIDTH: 136pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1pt solid" class="xl70" width="181">
    <p align="center"><font size="2" face="Times New Roman">　</font></p>
    </td>
    <td style="BORDER-BOTTOM: #f0f0f0; BORDER-LEFT: #f0f0f0; BACKGROUND-COLOR: white; WIDTH: 136pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1pt solid" class="xl72" width="181">
    <p align="center"><font size="2" face="Times New Roman">　</font></p>
    </td>
    <td style="BORDER-BOTTOM: #f0f0f0; BORDER-LEFT: #f0f0f0; BACKGROUND-COLOR: transparent; WIDTH: 136pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1pt solid" class="xl70" width="181">
    <p align="center"><font size="2" face="Times New Roman">　</font></p>
    </td>
    <td style="BORDER-BOTTOM: #f0f0f0; BORDER-LEFT: #f0f0f0; BACKGROUND-COLOR: transparent; WIDTH: 178pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1pt solid" class="xl81" width="237">
    <p align="center"><font size="2" face="Times New Roman">　</font></p>
    </td>
    </tr>
    <tr style="HEIGHT: 18pt; mso-height-source: userset" height="24">
    <td style="BORDER-BOTTOM: #f0f0f0; BORDER-LEFT: windowtext 1pt solid; BACKGROUND-COLOR: white; WIDTH: 64pt; HEIGHT: 18pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1pt solid" class="xl78" height="24" width="85">
    <p align="center"><strong><font size="2" face="宋体">myData0303</font></strong></p>
    </td>
    <td style="BORDER-BOTTOM: windowtext 1pt solid; BORDER-LEFT: #f0f0f0; BACKGROUND-COLOR: white; WIDTH: 64pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1pt solid" class="xl71" width="85">
    <p align="center"><font size="2" face="Times New Roman">Day</font></p>
    </td>
    <td style="BORDER-BOTTOM: windowtext 1pt solid; BORDER-LEFT: #f0f0f0; BACKGROUND-COLOR: white; WIDTH: 82pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1pt solid" class="xl71" width="109">
    <p align="center"><font size="2" face="Times New Roman">High temperature</font></p>
    </td>
    <td style="BORDER-BOTTOM: #f0f0f0; BORDER-LEFT: #f0f0f0; BACKGROUND-COLOR: transparent; WIDTH: 136pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1pt solid" class="xl76" width="181">
    <p align="center"><font size="2" face="宋体">myData0403</font></p>
    </td>
    <td style="BORDER-BOTTOM: #f0f0f0; BORDER-LEFT: #f0f0f0; BACKGROUND-COLOR: transparent; WIDTH: 136pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1pt solid" class="xl76" width="181">
    <p align="center"><font size="2" face="宋体">myData0503</font></p>
    </td>
    <td style="BORDER-BOTTOM: #f0f0f0; BORDER-LEFT: windowtext; BACKGROUND-COLOR: transparent; WIDTH: 136pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1pt solid" class="xl86" width="181">
    <p align="center"><font size="2"><font face="Times New Roman">myData0603</font></font></p>
    </td>
    <td style="BORDER-BOTTOM: #f0f0f0; BORDER-LEFT: windowtext; BACKGROUND-COLOR: transparent; WIDTH: 178pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1pt solid" class="xl82" width="237">
    <p align="center"><font size="2"><font face="Times New Roman">myData0703</font></font></p>
    </td>
    </tr>
    <tr style="HEIGHT: 23.25pt; mso-height-source: userset" height="31">
    <td style="BORDER-BOTTOM: #f0f0f0; BORDER-LEFT: windowtext 1pt solid; BACKGROUND-COLOR: white; WIDTH: 64pt; HEIGHT: 23.25pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1pt solid" class="xl79" height="31" width="85">
    <p align="center"><strong><font size="2" face="Times New Roman">myData0803</font></strong></p>
    </td>
    <td style="BORDER-BOTTOM: #f0f0f0; BORDER-LEFT: #f0f0f0; BACKGROUND-COLOR: white; WIDTH: 64pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1pt solid" class="xl72" width="85">
    <p align="center"><font class="font11" size="2" face="宋体">夜间</font></p>
    </td>
    <td style="BORDER-BOTTOM: #f0f0f0; BORDER-LEFT: #f0f0f0; BACKGROUND-COLOR: white; WIDTH: 82pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1pt solid" class="xl72" width="109">
    <p align="center"><font class="font11" size="2" face="宋体">低温</font></p>
    </td>
    <td style="BORDER-BOTTOM: black 1pt solid; BORDER-LEFT: windowtext 1pt solid; BACKGROUND-COLOR: transparent; WIDTH: 46pt; BORDER-TOP: windowtext; BORDER-RIGHT: windowtext 1pt solid" class="xl99" rowspan="2" width="61">
    <p align="center"><font size="2"><font face="Times New Roman">myData0903</font><font class="font11" face="宋体">℃</font></font></p>
    </td>
    <td style="BORDER-BOTTOM: #f0f0f0; BORDER-LEFT: #f0f0f0; BACKGROUND-COLOR: transparent; WIDTH: 136pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1pt solid" class="xl70" width="181">
    <p align="center"><font size="2" face="Times New Roman">myData1003</font></p>
    </td>
    <td style="BORDER-BOTTOM: #f0f0f0; BORDER-LEFT: #f0f0f0; BACKGROUND-COLOR: transparent; WIDTH: 136pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1pt solid" class="xl70" width="181">
    <p align="center"><font size="2" face="Times New Roman">myData1103</font></p>
    </td>
    <td style="BORDER-BOTTOM: #f0f0f0; BORDER-LEFT: windowtext; BACKGROUND-COLOR: transparent; WIDTH: 136pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1pt solid" class="xl73" width="181">
    <p align="center"><font size="2" face="Times New Roman">myData1203</font></p>
    </td>
    <td style="BORDER-BOTTOM: #f0f0f0; BORDER-LEFT: windowtext; BACKGROUND-COLOR: transparent; WIDTH: 178pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1pt solid" class="xl82" width="237">
    <p align="center"><font size="2" face="Times New Roman">myData1303</font></p>
    </td>
    </tr>
    <tr style="HEIGHT: 25.5pt; mso-height-source: userset" height="34">
    <td style="BORDER-BOTTOM: windowtext 1pt solid; BORDER-LEFT: windowtext 1pt solid; BACKGROUND-COLOR: white; WIDTH: 64pt; HEIGHT: 25.5pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1pt solid" class="xl74" height="34" width="85">
    <p align="center"><font size="2" face="Times New Roman">　</font></p>
    </td>
    <td style="BORDER-BOTTOM: windowtext 1pt solid; BORDER-LEFT: #f0f0f0; BACKGROUND-COLOR: white; WIDTH: 64pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1pt solid" class="xl71" width="85">
    <p align="center"><font size="2" face="Times New Roman">Night</font></p>
    </td>
    <td style="BORDER-BOTTOM: windowtext 1pt solid; BORDER-LEFT: #f0f0f0; BACKGROUND-COLOR: white; WIDTH: 82pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1pt solid" class="xl71" width="109">
    <p align="center"><font size="2" face="Times New Roman">Low temperature</font></p>
    </td>
    <td style="BORDER-BOTTOM: windowtext 1pt solid; BORDER-LEFT: #f0f0f0; BACKGROUND-COLOR: transparent; WIDTH: 136pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1pt solid" class="xl69" width="181">
    <p align="center"><font size="2" face="Times New Roman">　</font></p>
    </td>
    <td style="BORDER-BOTTOM: windowtext 1pt solid; BORDER-LEFT: #f0f0f0; BACKGROUND-COLOR: transparent; WIDTH: 136pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1pt solid" class="xl69" width="181">
    <p align="center"><font size="2" face="Times New Roman">　</font></p>
    </td>
    <td style="BORDER-BOTTOM: windowtext 1pt solid; BORDER-LEFT: #f0f0f0; BACKGROUND-COLOR: transparent; WIDTH: 136pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1pt solid" class="xl69" width="181">
    <p align="center"><font size="2" face="Times New Roman">　</font></p>
    </td>
    <td style="BORDER-BOTTOM: windowtext 1pt solid; BORDER-LEFT: #f0f0f0; BACKGROUND-COLOR: transparent; WIDTH: 178pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1pt solid" class="xl83" width="237">
    <p align="center"><font size="2" face="Times New Roman">　</font></p>
    </td>
    </tr>
    <tr style="HEIGHT: 13.5pt; mso-height-source: userset" height="18">
    <td style="BORDER-BOTTOM: #f0f0f0; BORDER-LEFT: windowtext 1pt solid; BACKGROUND-COLOR: white; WIDTH: 842pt; HEIGHT: 13.5pt; BORDER-TOP: windowtext 1pt solid; BORDER-RIGHT: black 1pt solid" class="xl101" height="18" width="1120" colspan="8">
    <font size="2" face="宋体"><strong>为降低对公司的影响范围和程度，请各部门做好以下工作：</strong></font></td>
    </tr>
    <tr style="HEIGHT: 14.25pt; mso-height-source: userset" height="19">
    <td style="BORDER-BOTTOM: windowtext 1pt solid; BORDER-LEFT: windowtext 1pt solid; BACKGROUND-COLOR: white; WIDTH: 842pt; HEIGHT: 14.25pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: black 1pt solid" class="xl104" height="19" width="1120" colspan="8">
    <strong><font size="2" face="Times New Roman">Please do the following job in order to reduce damage:</font></strong></td>
    </tr>
    <tr style="HEIGHT: 24.75pt; mso-height-source: userset" height="33">
    <td style="BORDER-BOTTOM: #f0f0f0; BORDER-LEFT: windowtext 1pt solid; BACKGROUND-COLOR: white; WIDTH: 842pt; HEIGHT: 24.75pt; BORDER-TOP: windowtext 1pt solid; BORDER-RIGHT: black 1pt solid" class="xl93" height="33" width="1120" colspan="8">
    <font size="2"><font face="Times New Roman">1.</font><font class="font11" face="宋体">各吊机使用部门做好露天吊机的锚固定，当风力达到六级以上或停工下班后，必须将吊机锚固定在防风位置，锁上夹轨器；</font></font></td>
    </tr>
    <tr style="HEIGHT: 25.5pt; mso-height-source: userset" height="34">
    <td style="BORDER-BOTTOM: windowtext 1pt solid; BORDER-LEFT: windowtext 1pt solid; BACKGROUND-COLOR: white; WIDTH: 842pt; HEIGHT: 25.5pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: black 1pt solid" class="xl96" height="34" width="1120" colspan="8">
    <font size="2" face="Times New Roman">Department that use crane in open air should make anchorage reinforcement during strong wind period, anchor in position and put on track lock when wind is over grade 6 or above when finish work;</font></td>
    </tr>
    <tr style="HEIGHT: 13.5pt; mso-height-source: userset" height="18">
    <td style="BORDER-BOTTOM: #f0f0f0; BORDER-LEFT: windowtext 1pt solid; BACKGROUND-COLOR: white; WIDTH: 842pt; HEIGHT: 13.5pt; BORDER-TOP: windowtext 1pt solid; BORDER-RIGHT: black 1pt solid" class="xl93" height="18" width="1120" colspan="8">
    <font size="2"><font face="Times New Roman">2.</font><font class="font11" face="宋体">设备部根据</font><font class="font10" face="Times New Roman">600</font><font class="font11" face="宋体">吨吊技术安全要求做好</font><font class="font10" face="Times New Roman">600</font><font class="font11" face="宋体">吨吊的防风工作；</font></font></td>
    </tr>
    <tr style="HEIGHT: 25.5pt; mso-height-source: userset" height="34">
    <td style="BORDER-BOTTOM: windowtext 1pt solid; BORDER-LEFT: windowtext 1pt solid; BACKGROUND-COLOR: white; WIDTH: 842pt; HEIGHT: 25.5pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: black 1pt solid" class="xl96" height="34" width="1120" colspan="8">
    <font size="2" face="Times New Roman">Hoisting Transportation Department to prepare windproof job in accordance with technical safety requirement of 600 tons crane;</font></td>
    </tr>
    <tr style="HEIGHT: 24.75pt; mso-height-source: userset" height="33">
    <td style="BORDER-BOTTOM: #f0f0f0; BORDER-LEFT: windowtext 1pt solid; BACKGROUND-COLOR: white; WIDTH: 842pt; HEIGHT: 24.75pt; BORDER-TOP: windowtext 1pt solid; BORDER-RIGHT: black 1pt solid" class="xl93" height="33" width="1120" colspan="8">
    <font size="2"><font face="Times New Roman">3.</font><font class="font11" face="宋体">大雨来临前请各项目做好防积水、防触电、防溢油等安全措施，如舱口加盖防雨棚、露天存放油桶加盖、露天用电设备加防雨淋措施等。并备好潜水泵、水带、砂包等防汛物资；</font></font></td>
    </tr>
    <tr style="HEIGHT: 51pt; mso-height-source: userset" height="68">
    <td style="BORDER-BOTTOM: windowtext 1pt solid; BORDER-LEFT: windowtext 1pt solid; BACKGROUND-COLOR: white; WIDTH: 842pt; HEIGHT: 51pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: black 1pt solid" class="xl96" height="68" width="1120" colspan="8">
    <font size="2" face="Times New Roman">All projects please make good preparation and anti-water, anti-electric shock, anti-oil spills measures etc. before the rain, for example: put on anti-canopy an on hatch, put on cover onto oil barrel in open air, put on
     anti-rain measures on electrical equipment in open etc as well as prepare flood prevention materials such as submersible motor pump, hose, sand bag etc.</font></td>
    </tr>
    <tr style="HEIGHT: 13.5pt; mso-height-source: userset" height="18">
    <td style="BORDER-BOTTOM: #f0f0f0; BORDER-LEFT: windowtext 1pt solid; BACKGROUND-COLOR: white; WIDTH: 842pt; HEIGHT: 13.5pt; BORDER-TOP: windowtext 1pt solid; BORDER-RIGHT: black 1pt solid" class="xl93" height="18" width="1120" colspan="8">
    <font size="2"><font face="Times New Roman">4.</font><font class="font11" face="宋体">请生产管理部与</font><font class="font10" face="Times New Roman">HSE</font><font class="font11" face="宋体">部做好各登船梯口和危险部位的防摔倒措施.</font></font></td>
    </tr>
    <tr style="HEIGHT: 25.5pt; mso-height-source: userset" height="34">
    <td style="BORDER-BOTTOM: windowtext 1pt solid; BORDER-LEFT: windowtext 1pt solid; BACKGROUND-COLOR: white; WIDTH: 842pt; HEIGHT: 25.5pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: black 1pt solid" class="xl96" height="34" width="1120" colspan="8">
    <font size="2" face="Times New Roman">Production Department and HSE department prepare anti-skid measures on boarding stairs and other dangerous areas;</font></td>
    </tr>
    <tr style="HEIGHT: 13.5pt; mso-height-source: userset" height="18">
    <td style="BORDER-BOTTOM: #f0f0f0; BORDER-LEFT: windowtext 1pt solid; BACKGROUND-COLOR: white; WIDTH: 842pt; HEIGHT: 13.5pt; BORDER-TOP: windowtext 1pt solid; BORDER-RIGHT: black 1pt solid" class="xl93" height="18" width="1120" colspan="8">
    <font size="2"><font face="Times New Roman">5.</font><font class="font11" face="宋体">大风、雷雨期间暂停一切室外作业，并做好防护工作，以策安全；</font></font></td>
    </tr>
    <tr style="HEIGHT: 14.25pt; mso-height-source: userset" height="19">
    <td style="BORDER-BOTTOM: windowtext 1pt solid; BORDER-LEFT: windowtext 1pt solid; BACKGROUND-COLOR: white; WIDTH: 842pt; HEIGHT: 14.25pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: black 1pt solid" class="xl96" height="19" width="1120" colspan="8">
    <font size="2" face="Times New Roman">Stop all outdoor operations during period of strong wind and make good preparation for safety reason;</font></td>
    </tr>
    <tr style="HEIGHT: 13.5pt; mso-height-source: userset" height="18">
    <td style="BORDER-BOTTOM: #f0f0f0; BORDER-LEFT: windowtext 1pt solid; BACKGROUND-COLOR: white; WIDTH: 842pt; HEIGHT: 13.5pt; BORDER-TOP: windowtext 1pt solid; BORDER-RIGHT: black 1pt solid" class="xl93" height="18" width="1120" colspan="8">
    <font size="2"><font face="Times New Roman">6.</font><font class="font11" face="宋体">其他部门也请根据各自情况做好异常天气期间的防风、防雨、防汛工作；</font></font></td>
    </tr>
    <tr style="HEIGHT: 25.5pt; mso-height-source: userset" height="34">
    <td style="BORDER-BOTTOM: windowtext 1pt solid; BORDER-LEFT: windowtext 1pt solid; BACKGROUND-COLOR: white; WIDTH: 842pt; HEIGHT: 25.5pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: black 1pt solid" class="xl96" height="34" width="1120" colspan="8">
    <font size="2" face="Times New Roman">Other departments should do relevant wind proof job, rain proof and flood job according to their own situations during abnormal period;</font></td>
    </tr>
    <tr style="HEIGHT: 13.5pt; mso-height-source: userset" height="18">
    <td style="BORDER-BOTTOM: #f0f0f0; BORDER-LEFT: windowtext 1pt solid; BACKGROUND-COLOR: white; WIDTH: 842pt; HEIGHT: 13.5pt; BORDER-TOP: windowtext 1pt solid; BORDER-RIGHT: black 1pt solid" class="xl93" height="18" width="1120" colspan="8">
    <font size="2"><font face="Times New Roman">7.</font><font class="font11" face="宋体">各相关部门留厂值班的三防人员要坚守岗位</font><font class="font10" face="Times New Roman">,</font><font class="font11" face="宋体">发现异常情况要及时处理和报告。</font></font></td>
    </tr>
    <tr style="HEIGHT: 25.5pt; mso-height-source: userset" height="34">
    <td style="BORDER-BOTTOM: windowtext 1pt solid; BORDER-LEFT: windowtext 1pt solid; BACKGROUND-COLOR: white; WIDTH: 842pt; HEIGHT: 25.5pt; BORDER-TOP: #f0f0f0; BORDER-RIGHT: black 1pt solid" class="xl96" height="34" width="1120" colspan="8">
    <font size="2" face="Times New Roman">Three-national defense people on duty of all relevant departments should keep to their posts; any abnormal situation should be processed and reported in time.</font></td>
    </tr>
    <tr style="HEIGHT: 14.25pt" height="19">
    <td style="BORDER-BOTTOM: windowtext 1pt solid; BORDER-LEFT: windowtext 1pt solid; BACKGROUND-COLOR: white; WIDTH: 842pt; HEIGHT: 14.25pt; BORDER-TOP: windowtext 1pt solid; BORDER-RIGHT: black 1pt solid" class="xl90" height="19" width="1120" colspan="8">
    <p align="right"><strong><font size="2" face="Times New Roman">HSE</font></strong></p>
    </td>
    </tr>
    </tbody>
    </table>
    </p>
    </span></div>
    <br>
    <hr>
    <font face="Arial" color="Gray" size="2">CONFIDENTIALITY NOTICE<br>
    Information in this message is confidential and may be privileged. It is intended solely for the person to whom it is addressed. If you are not intended recipient, please notify the sender and delete the message and any other record of it from your system immediately.<br>
    </font>
    </body>
    </html>
    '''
    weekList=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    weekListC=['星期一','星期二','星期三','星期四','星期五','星期六','星期天']
    weatherDict={"阴":"overcast",'晴':'clear','雷阵雨':'thunder shower',
    '多云':'cloudy','多云':'cloudy','阵雨':'shower','小雨':'light rain','小到中雨':'light to moderate rain','雨夹雪':'sleet','小雪':'light snow','中雪':'moderate snow','大雪':'heavy snow'}
    windDict={'东风':'east wind','东北风':'northeast wind','北风':'north wind','西北风':'northwest wind',
    '西风':'west wind','西南风':'southwest wind','南风':'south wind','东南风':'southeast wind'}
    t=web
    if t!= None:
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

        out = open(str(datetime.datetime.now().date())+'.html','w')#,encoding='utf-8')
        out.write(t)
        out.close()
    


 
if __name__ == '__main__':
    landData = landWeather()[:3]
    seaData = seaWeather()
    #landData.append(seaData)
    #print(seaData)
    mailData(landData,seaData)
