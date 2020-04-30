#-*-coding:utf-8-*-

import requests, re, json
import parser
import urllib
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from urllib.request import urlopen
import youtube_dl

def yt(name):
    url = "https://www.youtube.com/results?search_query=" + name
    headers = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36' }
    html = requests.get(url, headers=headers)

    soup = BeautifulSoup(html.text, 'html.parser')
    videos = soup.findAll('div', attrs={'class':'yt-lockup-content'})

    result = []

    for video in videos:
        result1 = {}
        name = video.find(dir='ltr').get('title')
        link = 'https://www.youtube.com'+video.find(class_='yt-uix-tile-link').get('href')
        result1['name'] = name
        result1['link'] = link

        result.append(result1)

    return result

print(yt('Coffin dance'))