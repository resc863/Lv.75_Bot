import requests
import json
import datetime

key = ""
url = "http://api.openweathermap.org/data/2.5/forecast?q=busan&cnt=10&units=metric&lang=kr&APPID="+key

html = requests.get(url).text
data = json.loads(html)

name = data['city']['name']
weather = data['list']

print(name)

for i in weather:
    date = datetime.datetime.fromtimestamp(i['dt']).strftime('%Y-%m-%d %H:%M:%S')
    print("예보 시각: "+date)
    temp = i['main']['temp']
    print("기온: "+str(temp))
    feel = i['main']['feels_like']
    print("체감 기온: "+str(feel))
    humidity = i['main']['humidity']
    print("습도: "+str(humidity))
    cloud = i['weather'][0]['description']
    print("구름: "+cloud)
    print("="*20)
