#-*-coding:utf-8-*-

import requests, re, json
import parser
import urllib
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from urllib.request import urlopen
import youtube_dl

def mask(location):
    location = urllib.parse.quote(location)
    url = "https://8oi9s0nnth.apigw.ntruss.com/corona19-masks/v1/storesByAddr/json?address="+location
    

    html = urlopen(url).read().decode('utf-8')
    data = json.loads(html).get('stores')

    return data


mask('부산광역시 해운대구')
