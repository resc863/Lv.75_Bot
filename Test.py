import requests, re
import parser
import urllib
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import youtube_dl

def stid(name,n):
    key = "0XeO7nbthbiRoMUkYGGah20%2BfXizwc0A6BfjrkL6qhh2%2Fsl8j9PzfSLGKnqR%2F1v%2F%2B6AunxntpLfoB3Ryd3OInQ%3D%3D"
    name = urllib.parse.quote(name)
    url = "http://61.43.246.153/openapi-data/service/busanBIMS2/busStop?serviceKey="+key+"&pageNo=1&numOfRows=10&bstopnm="+name
    doc = urllib.request.urlopen(url)
    xml1 = BeautifulSoup(doc,"html.parser")
    stopid2 = xml1.findAll('bstopid',string=True)

    if n == 1:
        stopid1 = str(stopid2[0])
        stopid = stopid1[9:18]
    elif n == 2:
        stopid1 = str(stopid2[1])
        stopid = stopid1[9:18]
    return stopid

def info(station):
    key = "0XeO7nbthbiRoMUkYGGah20%2BfXizwc0A6BfjrkL6qhh2%2Fsl8j9PzfSLGKnqR%2F1v%2F%2B6AunxntpLfoB3Ryd3OInQ%3D%3D"
    url = "http://61.43.246.153/openapi-data/service/busanBIMS2/stopArr?serviceKey="+key+"&bstopid="+stid(station, 1)
    url1 = "http://61.43.246.153/openapi-data/service/busanBIMS2/stopArr?serviceKey="+key+"&bstopid="+stid(station, 2)

    inf1 = urllib.request.urlopen(url)
    info1 = BeautifulSoup(inf1, "html.parser")

    print("*"*20)
    
    for item in info1.findAll('item'):
        
        min1 = ""
        station1=""

        if item.min1 == None:
            min1 = "정보가 없슴니다."
        else:
            min1 = item.min1.string

        if item.station1 == None:
            
            station1 = "정보가 없슴니다."
        else:
            station1 = item.station1.string
        
        print("버스 번호:",item.lineno.string)
        print("도착 시간:",min1)
        print("남은 정류소 수:",station1)
        print("="*20)

    inf2 = urllib.request.urlopen(url1)
    info2 = BeautifulSoup(inf2, "html.parser")

    print("*"*30)

    for item in info2.findAll('item'):
        
        min1 = ""
        station1=""

        if item.min1 == None:
            min1 = "정보가 없슴니다."
        else:
            min1 = item.min1.string

        if item.station1 == None:
            
            station1 = "정보가 없슴니다."
        else:
            station1 = item.station1.string

        print("버스 번호:",item.lineno.string)
        print("도착 시간:",min1)
        print("남은 정류소 수:",station1)
        print("="*20)
        
    return None

info("동부아파트")

def get_info():
    name = learn
    enc_name = urllib.parse.quote(name)
    url = "https://r6.tracker.network/profile/pc/"+enc_name
    html = requests.get(url)
    bs = BeautifulSoup(html.text, "html.parser")
    bs_value = bs.find_all("div",{"class": "trn-defstat__value"})
    
    lvl1 = bs_value[0]
    lvl2 = lvl1.text
    print(lvl2)

    high_mmr1 = bs_value[1]
    high_mmr2 = high_mmr1.text
    print(high_mmr2)

    rank = bs_value[2]
    rank = rank.text
    print(rank)

    topop1 = bs_value[4]
    print(topop1)

    pvpwin1 = bs_value[5]
    pvpwin2 = pvpwin1.text
    print(pvpwin2)

    winratio1 = bs_value[6]
    winratio2 = winratio1.text
    print(winratio2)

    pvpkill1 = bs_value[7]
    pvpkill2 = pvpkill1.text
    print(pvpkill2)

    pvpkd1 = bs_value[8]
    pvpkd2 = pvpkd1.text
    print(pvpkd2)

    time1 = bs_value[11]
    time2 = time1.text
    print(time2)

learn = "Lv.99_B0SS"
get_info()
