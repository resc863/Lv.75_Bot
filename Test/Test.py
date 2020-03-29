import requests, re
import parser
import urllib
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import youtube_dl

def op_info(name, op):
    i = 18
    enc_name = urllib.parse.quote(name)
    url = "https://r6.tracker.network/profile/pc/"+enc_name+"/operators"
    html = requests.get(url)
    bs = BeautifulSoup(html.text, "html.parser")
    n = bs.find_all("td",{"class": "trn-text--right"})
    name1 = bs.find_all("span")
    a = ""

    while a != op:
        i = i+1
        a = name1[i].text
    
    n1 = name1[i].text
    result="오퍼 이름: "+n1+"\n"

    j = (i-19)*12

    time = n[j].text
    result = result + "플레이타임: "+n[j].text+"\n"

    kills = n[j+1].text
    result = result + "킬: "+n[j+1].text+"\n"

    death = n[j+2].text
    result = result + "데스: "+n[j+2].text+"\n"

    kd = n[j+3].text
    result = result + "K/D: "+n[j+3].text+"\n"

    win = n[j+4].text
    result = result + "승: "+n[j+4].text+"\n"

    lose = n[j+5].text
    result = result + "패: "+n[j+5].text+"\n"

    winper = n[j+6].text
    result = result + "승률: "+n[j+6].text+"\n"

    melee = n[j+7].text
    result = result + "근접 킬: "+n[j+7].text+"\n"

    head = n[j+8].text
    result = result + "헤드: "+n[j+8].text+"\n"

    dbno = n[j+9].text
    result = result + "부상: "+n[j+9].text+"\n"

    xp = n[j+10].text
    result = result + "경험치: "+n[j+10].text+"\n"

    opstat = n[j+11].text
    result = result + "오퍼 스탯: "+n[j+11].text+"\n"

    return result
 
print("=================================================")
print("=                                               =")
print("=        레인보우 식스 전적검색 시스템          =")
print("=                                               =")
print("=================================================")
q1 = input("닉네임 입력: ")
q2 = input("오퍼 입력: ")
print("\n검색중...\n")
a = op_info(q1, q2)
print(a)
