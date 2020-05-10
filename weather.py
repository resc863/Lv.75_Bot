import requests
import json
import datetime

key = "23fb1206721ca9dd443fbc3f6b4f20ec"
url = "http://api.openweathermap.org/data/2.5/forecast?q=busan&units=metric&lang=kr&APPID="+key

html = requests.get(url).text
data = json.loads(html)

name = data['city']['name']
weather = data['list']

print(name)

for i in weather:
    date = datetime.datetime.fromtimestamp(i['dt']).strftime('%Y-%m-%d %H:%M:%S')
    print(date)
    print(i['main'])

