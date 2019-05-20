import urllib
import requests 
import bs4
from bs4 import BeautifulSoup

name = "Just Another Order"
enc_name = urllib.parse.quote(name)
url = "https://m.youtube.com/results?search_query="+enc_name
html = requests.get(url)
bs = BeautifulSoup(html.text, "html.parser")
bs_value = bs.find_all("span","aria-label")
print(bs_value[5])
