import requests, re
import parser
import urllib
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import youtube_dl

def get_info(name):
    enc_name = urllib.parse.quote(name)
    url = "https://r6.op.gg/search?search="+enc_name
    html = requests.get(url)
    len1 = len(name)
    bs = BeautifulSoup(html.text, "html.parser")
    n = bs.find_all("div",{"class": "text-center mt-4"})
    
    n1 = n[0]
    n2 = n1.text
    n3 = n2.strip()
    name1 = n3[0:len1]
    print(name1)
 
get_info("Lv.99_B0SS")
