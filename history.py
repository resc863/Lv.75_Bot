import requests, re
import parser
import urllib
from bs4 import BeautifulSoup

def get_info():
    name = "Lv.99_B0SS"
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


get_info()
