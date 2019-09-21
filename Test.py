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
    print(n1)

    j = (i-19)*12

    time = n[j].text
    print(time)

    kills = n[j+1].text
    print(kills)

    death = n[j+2].text
    print(death)

    kd = n[j+4].text
    print(kd)

    win = n[j+5].text
    print(win)

    lose = n[j+6].text
    print(lose)

    winper = n[j+7].text
    print(winper)

    melee = n[j+8].text
    print(melee)

    head = n[j+9].text
    print(head)

    dbno = n[j+10].text
    print(dbno)

    xp = n[j+11].text
    print(xp)

    opstat = n[j+12].text
    print(opstat)
 
op_info("Lv.99_B0SS", "ASH")
