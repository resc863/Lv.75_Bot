import asyncio
import discord
import random
import datetime
import requests, re
import youtube_dl
import ffmpeg
import urllib
import urllib.request
import bs4
import os
import sys
import json
import parser
from urllib.request import urlopen, Request
from discord import Member
from discord.ext import commands
from discord.utils import get
from bs4 import BeautifulSoup #패키지 설치 필수

client = discord.Client()

token = os.environ["bottoken"]
schcode = ""

def search_book(keyword):
    base_url = 'https://www.aladin.co.kr/search/wsearchresult.aspx?'
    encoding_type = 'EUC-KR'
    book_list = []
    params = {'SearchTarget':'DVD','SortOrder':11}
    params['SearchWord'] = keyword

    url =  base_url + urllib.parse.urlencode(params, encoding = encoding_type)
    url_get = requests.get(url)
    soup = BeautifulSoup(url_get.content, 'lxml')
    items = soup.find_all(class_='ss_book_box')
    list = []

    for item in items:
        if item.find(class_='ss_book_list') is None:
            continue
        name = item.find(class_="bo3").string
        info = {}
        info['name']=name

        data1 = item.find(class_="ss_book_list").find_next('ul').find_all('li')[1].find_all('a')
        data = ""

        try:
            price = item.find(class_="ss_book_list").find_next('ul').find_all('li')[2].find('span').string
            info['price'] = price
        except:
            info['price'] = 'None'
        
        for i in data1:
            data = data + i.string + " "

        info['data']=data

        list.append(info)
    return list

def inf():
    url = 'http://www.yes24.com/Product/Goods/84907426?scode=032&OzSrank=13'
    html = requests.get(url).text

    soup = BeautifulSoup(html, 'html.parser')

    result = "Yes24 정보\n"

    book_name = '#yDetailTopWrap > div.topColRgt > div.gd_infoTop > div > h2'
    book = soup.select(book_name)
    result = result + "타이틀명: "+book[0].text+"\n"

    release_date = '#yDetailTopWrap > div.topColRgt > div.gd_infoTop > span.gd_pubArea > span'
    release = soup.select(release_date)

    for i in release:
        date = i.get('class')

        for j in date:
            if j == 'gd_date':
                result = result + "출시일 : "+i.text+"\n"

    rating = '#yDetailTopWrap > div.topColRgt > div.gd_infoTop > span.gd_ratingArea > span'
    rating1 = soup.select(rating)
    result = result + "평가: "+rating1[0].text

    price_info = '#yDetailTopWrap > div.topColRgt > div.gd_infoBot > div.gd_infoTbArea > div:nth-child(3) > table > tbody > tr:nth-child(1) > td > span > em'
    price = soup.select(price_info)
    result = result + "정가: "+price[0].text+"\n"

    sale_price = '#yDetailTopWrap > div.topColRgt > div.gd_infoBot > div.gd_infoTbArea > div:nth-child(3) > table > tbody > tr.accentRow > td > span > em'
    sale = soup.select(sale_price)
    result = result + "할인가: " +sale[0].text

    result = result + "\n\n"


    url = 'https://www.aladin.co.kr/search/wsearchresult.aspx?SearchTarget=DVD&KeyWord=%B0%DC%BF%EF%BF%D5%B1%B9+2&KeyRecentPublish=0&OutStock=0&ViewType=Detail&CustReviewCount=0&CustReviewRank=0&KeyFullWord=%B0%DC%BF%EF%BF%D5%B1%B9+2&KeyLastWord=%B0%DC%BF%EF%BF%D5%B1%B9+2&CategorySearch=&chkKeyTitle=&chkKeyAuthor=&chkKeyPublisher=&chkKeyISBN=&chkKeyTag=&chkKeyTOC=&chkKeySubject='
    html = requests.get(url).text

    soup = BeautifulSoup(html, 'html.parser')

    result = result + "알라딘 정보\n"

    dvdlist = search_book('겨울왕국2')

    for i in dvdlist:
        result = result + "타이틀명: "+i['name']+"\n"
        result = result + "가격: "+i['price']+"\n"
        result = result + "정보: "+i['data']+"\n"
        result = result + "\n\n"
    
    return result

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

def lineid(lineno):    
    lineurl = "http://61.43.246.153/openapi-data/service/busanBIMS2/busInfo?lineno="+lineno+"&serviceKey=0XeO7nbthbiRoMUkYGGah20%2BfXizwc0A6BfjrkL6qhh2%2Fsl8j9PzfSLGKnqR%2F1v%2F%2B6AunxntpLfoB3Ryd3OInQ%3D%3D"
    lineid2 = urllib.request.urlopen(lineurl)
    lineid1 = BeautifulSoup(lineid2, "html.parser")
    lineid0 = lineid1.find('item')
    lineid = lineid0.lineid.string

    return lineid

def nextstop(no, lineno):
    lineid1 = lineid(lineno)
    url = "http://61.43.246.153/openapi-data/service/busanBIMS2/busInfoRoute?lineid="+lineid1+"&serviceKey=0XeO7nbthbiRoMUkYGGah20%2BfXizwc0A6BfjrkL6qhh2%2Fsl8j9PzfSLGKnqR%2F1v%2F%2B6AunxntpLfoB3Ryd3OInQ%3D%3D"
    text = urllib.request.urlopen(url)
    soup = BeautifulSoup(text, "html.parser")
    nextidx = 0

    for item in soup.findAll('item'):
        bstop = ""
        
        if item.arsno == None:
            
            bstop = "정보가 없습니다."
        else:
            bstop = item.arsno.string
            
        curidx = int(item.bstopidx.string)
        
        if bstop == no:
            nextidx = curidx
            nextidx = nextidx + 1
            
        elif curidx == nextidx:
            nextstop = item.bstopnm.string
            return nextstop

def get_diet(code, ymd, weekday):
    schMmealScCode = code #int 1조식2중식3석식
    schYmd = ymd #str 요청할 날짜 yyyy.mm.dd
    if weekday == 5 or weekday == 6: #토요일,일요일 버림
        element = " " #공백 반환
    else:
        num = weekday + 1 #int 요청할 날짜의 요일 0월1화2수3목4금5토6일 파싱한 데이터의 배열이 일요일부터 시작되므로 1을 더해줍니다.
        URL = (
                "http://stu.pen.go.kr/sts_sci_md01_001.do?"
                "schulCode="+schcode+"&schulCrseScCode=4"
                "&schulKndScCode=04"
                "&schMmealScCode=%d&schYmd=%s" % (schMmealScCode, schYmd)
            )
        #http://stu.pen.go.kr/ 관할 교육청 주소 확인해주세요.
        #schulCode= 학교고유코드
        #schulCrseScCode= 1유치원2초등학교3중학교4고등학교
        #schulKndScCode= 01유치원02초등학교03중학교04고등학교

        #기존 get_html 함수부분을 옮겨왔습니다.
        html = ""
        resp = requests.get(URL)
        if resp.status_code == 200 : #사이트가 정상적으로 응답할 경우
            html = resp.text
        soup = BeautifulSoup(html, 'html.parser')
        element_data = soup.find_all("tr")
        element_data = element_data[2].find_all('td')
        try:
            element = str(element_data[num])

            #filter
            element_filter = ['[', ']', '<td class="textC last">', '<td class="textC">', '</td>', '&amp;', '(h)', '.']
            for element_string in element_filter :
                element = element.replace(element_string, '')
            #줄 바꿈 처리
            element = element.replace('<br/>', '\n')
            #모든 공백 삭제
            element = re.sub(r"\d", "", element)

        #급식이 없을 경우
        except:
            element = " " # 공백 반환
    return element

def get_code(school_name):
    result = {'high': {}}
    code = ""

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    }

    data = {
        'HG_CD': '',
        'SEARCH_KIND': '',
        'HG_JONGRYU_GB': '',
        'GS_HANGMOK_CD': '',
        'GS_HANGMOK_NM': '',
        'GU_GUN_CODE': '',
        'SIDO_CODE': '',
        'GUGUN_CODE': '',
        'SRC_HG_NM': school_name
    }

    response = json.loads(requests.post('https://www.schoolinfo.go.kr/ei/ss/Pneiss_a01_l0.do',
                                        headers=headers, data=data).text)

    for i in range(2, 6):
        sch = response[f'schoolList0{i}']
        if sch:
            for c in range(0, len(sch)):
                code = sch[c]['SCHUL_CODE']

    return code

def check_queue(id):
    if queues[id] != []:
        player = queues[id].pop(0)
        players[id] = player
        player.start()


async def print_get_meal(local_date, local_weekday, message):
        l_diet = get_diet(2, local_date, local_weekday)
        d_diet = get_diet(3, local_date, local_weekday)

        if len(l_diet) == 1:
            embed = discord.Embed(title="No Meal", description="급식이 없습니다.", color=0x00ff00)
            await client.send_message(message.channel, embed=embed)
        elif len(d_diet) == 1:
            lunch = local_date + " 중식\n" + l_diet
            embed = discord.Embed(title="Lunch", description=lunch, color=0x00ff00)
            await client.send_message(message.channel, embed=embed)
        else:
            lunch = local_date + " 중식\n" + l_diet
            dinner = local_date + " 석식\n" + d_diet
            embed= discord.Embed(title="Lunch", description=lunch, color=0x00ff00)
            await client.send_message(message.channel, embed=embed)
            embed = discord.Embed(title="Dinner", description=dinner, color=0x00ff00)
            await client.send_message(message.channel, embed=embed)
            
@client.event
async def on_ready():
    print("Logged in ") 
    print(client.user.name)
    print(client.user.id)
    print("===============")
    await client.change_presence(game=discord.Game(name=":D", type=1))
    channel = client.get_channel('579305105107714057')
    message = await client.send_message(channel, "공지를 읽고 다음 이모지를 누르세요...")
    await client.add_reaction(message, emoji="\U0001F44C")
    
@client.event
async def on_message(message):
    now = datetime.datetime.now()

    if message.author.bot: 
        return None 

    id = message.author.id 
    channel = message.channel

    a = str(random.randint(1,100))

    if message.content.startswith('반갑습니다'): 
        await client.send_message(channel, "반갑습니다 <@"+id+"> 님" )
        
    if message.content.startswith('블루레이'): 
        await client.send_message(channel, inf())
        

    if message.content.startswith('위대하신'): 
        await client.send_message(channel, "수령 동지를 위하여" )
        
    if message.content.startswith('오늘의 운세는?'): 
        await client.send_message(channel, "<@"+id+"> 님의 운은 "+a+"%입니다")

    if message.content.startswith('!명령어'):
        embed = discord.Embed(title="Lv.75 Bot 명령어 목록 ", description="반갑습니다 = 반갑습니다 id 님")
        embed.add_field(name="날씨", value="날씨 + 지역명 : 현재 지역 날씨", inline=False)
        embed.add_field(name="급식", value="오늘 급식은? > 학교 이름 입력 > 날짜 입력 : 급식 식단 출력 (부산광역시교육청 전용)", inline=False)
        embed.add_field(name="실시간 검색어 순위", value="실검 : 현재 실시간 검색어 순위", inline=False)
        await client.send_message(message.channel, embed=embed)

    if message.content.startswith('지금 시간은?'):
        embed = discord.Embed(title="현재 시각 ", description="지금 시간은")
        embed.set_footer(text = str(now.year) + "년 " + str(now.month) + "월 " + str(now.day) + "일 | " + str(now.hour) + ":" + str(now.minute) + ":" + str(now.second))
        await client.send_message(message.channel, embed=embed)

    if message.content.startswith('오늘 급식은?'):
        place = '학교명을 입력하세요'
        request_e = discord.Embed(title="Send to Me", description=place, color=0xcceeff)
        await client.send_message(message.channel, embed=request_e)
        schplace = await client.wait_for_message(timeout=15.0, author=message.author)
        schplace = str(schplace.content) #사용 가능한 형식으로 변형
        print(schplace)
        print(get_code(schplace))

        global schcode #전역 변수 설정

        schcode = get_code(schplace)

        request = '날짜를 보내주세요...'
        request_e = discord.Embed(title=schplace, description=request, color=0xcceeff)
        await client.send_message(message.channel, embed=request_e)
        meal_date = await client.wait_for_message(timeout=15.0, author=message.author)

        #입력이 없을 경우
        if meal_date is None:
            longtimemsg = discord.Embed(title="In 15sec", description='15초내로 입력해주세요. 다시시도 : $g', color=0xff0000)
            await client.send_message(message.channel, embed=longtimemsg)
            return

        meal_date = str(meal_date.content) # 171121
        meal_date = '20' + meal_date[:2] + '.' + meal_date[2:4] + '.' + meal_date[4:6] # 2017.11.21

        s = meal_date.replace('.', ', ') # 2017, 11, 21

        #한자리수 달인 경우를 해결하기위함
        if int(s[6:8]) < 10:
            s = s.replace(s[6:8], s[7:8])

        ss = "datetime.datetime(" + s + ").weekday()"
        try:
            whatday = eval(ss)
        except:
            warnning = discord.Embed(title="Plz Retry", description='올바른 값으로 다시 시도하세요 : $g', color=0xff0000)
            await client.send_message(message.channel, embed=warnning)
            return

        await print_get_meal(meal_date, whatday, message)
        
    if message.content.startswith("날씨"):
        learn = message.content.split(" ")
        location = learn[1]
        enc_location = urllib.parse.quote(location+'날씨')
        hdr = {'User-Agent': 'Mozilla/5.0'}
        url = 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=' + enc_location
        print(url)
        req = Request(url, headers=hdr)
        html = urllib.request.urlopen(req)
        bsObj = bs4.BeautifulSoup(html, "html.parser")
        todayBase = bsObj.find('div', {'class': 'main_info'})

        todayTemp1 = todayBase.find('span', {'class': 'todaytemp'})
        todayTemp = todayTemp1.text.strip()  # 온도
        print(todayTemp)

        todayValueBase = todayBase.find('ul', {'class': 'info_list'})
        todayValue2 = todayValueBase.find('p', {'class': 'cast_txt'})
        todayValue = todayValue2.text.strip()  # 밝음,어제보다 ?도 높거나 낮음을 나타내줌
        print(todayValue)

        todayFeelingTemp1 = todayValueBase.find('span', {'class': 'sensible'})
        todayFeelingTemp = todayFeelingTemp1.text.strip()  # 체감온도
        print(todayFeelingTemp)

        todayMiseaMongi1 = bsObj.find('div', {'class': 'sub_info'})
        todayMiseaMongi2 = todayMiseaMongi1.find('div', {'class': 'detail_box'})
        todayMiseaMongi3 = todayMiseaMongi2.find('dd')
        todayMiseaMongi = todayMiseaMongi3.text  # 미세먼지
        print(todayMiseaMongi)

        tomorrowBase = bsObj.find('div', {'class': 'table_info weekly _weeklyWeather'})
        tomorrowTemp1 = tomorrowBase.find('li', {'class': 'date_info'})
        tomorrowTemp2 = tomorrowTemp1.find('dl')
        tomorrowTemp3 = tomorrowTemp2.find('dd')
        tomorrowTemp = tomorrowTemp3.text.strip()  # 오늘 오전,오후온도
        print(tomorrowTemp)

        tomorrowAreaBase = bsObj.find('div', {'class': 'tomorrow_area'})
        tomorrowMoring1 = tomorrowAreaBase.find('div', {'class': 'main_info morning_box'})
        tomorrowMoring2 = tomorrowMoring1.find('span', {'class': 'todaytemp'})
        tomorrowMoring = tomorrowMoring2.text.strip()  # 내일 오전 온도
        print(tomorrowMoring)

        tomorrowValue1 = tomorrowMoring1.find('div', {'class': 'info_data'})
        tomorrowValue = tomorrowValue1.text.strip()  # 내일 오전 날씨상태, 미세먼지 상태
        print(tomorrowValue)

        tomorrowAreaBase = bsObj.find('div', {'class': 'tomorrow_area'})
        tomorrowAllFind = tomorrowAreaBase.find_all('div', {'class': 'main_info morning_box'})
        tomorrowAfter1 = tomorrowAllFind[1]
        tomorrowAfter2 = tomorrowAfter1.find('p', {'class': 'info_temperature'})
        tomorrowAfter3 = tomorrowAfter2.find('span', {'class': 'todaytemp'})
        tomorrowAfterTemp = tomorrowAfter3.text.strip()  # 내일 오후 온도
        print(tomorrowAfterTemp)

        tomorrowAfterValue1 = tomorrowAfter1.find('div', {'class': 'info_data'})
        tomorrowAfterValue = tomorrowAfterValue1.text.strip()

        print(tomorrowAfterValue)  # 내일 오후 날씨상태,미세먼지

        embed = discord.Embed(
            title=learn[1]+ ' 날씨 정보',
            description=learn[1]+ ' 날씨 정보입니다.',
            colour=discord.Colour.gold()
        )
        embed.add_field(name='현재온도', value=todayTemp+'˚', inline=False)  # 현재온도
        embed.add_field(name='체감온도', value=todayFeelingTemp, inline=False)  # 체감온도
        embed.add_field(name='현재상태', value=todayValue, inline=False)  # 밝음,어제보다 ?도 높거나 낮음을 나타내줌
        embed.add_field(name='현재 미세먼지 상태', value=todayMiseaMongi, inline=False)  # 오늘 미세먼지
        embed.add_field(name='오늘 오전/오후 날씨', value=tomorrowTemp, inline=False)  # 오늘날씨 # color=discord.Color.blue()
        embed.add_field(name='**----------------------------------**',value='**----------------------------------**', inline=False)  # 구분선
        embed.add_field(name='내일 오전온도', value=tomorrowMoring+'˚', inline=False)  # 내일오전날씨
        embed.add_field(name='내일 오전날씨상태, 미세먼지 상태', value=tomorrowValue, inline=False)  # 내일오전 날씨상태
        embed.add_field(name='내일 오후온도', value=tomorrowAfterTemp + '˚', inline=False)  # 내일오후날씨
        embed.add_field(name='내일 오후날씨상태, 미세먼지 상태', value=tomorrowAfterValue, inline=False)  # 내일오후 날씨상태



        await client.send_message(message.channel,embed=embed)

    if message.content.startswith('실검'):
        html = requests.get('https://www.naver.com').text

        soup = BeautifulSoup(html, 'html.parser')
        element = soup.select('.PM_CL_realtimeKeyword_rolling span[class*=ah_k]')

        embed = discord.Embed(title="현재 실시간 검색어 순위 ")
        for idx, title in enumerate(element, 1):
           print(idx, title.text)
           embed.add_field(name=str(idx), value=title.text, inline=False)
        await client.send_message(message.channel, embed=embed)

    if message.content.startswith("롤"):
        learn = message.content.split(" ")
        name = learn[1]
        enc_name = urllib.parse.quote(name)

        url = "http://www.op.gg/summoner/userName=" + enc_name
        html = urllib.request.urlopen(url)

        bsObj = bs4.BeautifulSoup(html, "html.parser")
        rank1 = bsObj.find("div", {"class": "TierRankInfo"})
        rank2 = rank1.find("div", {"class": "TierRank"})
        rank4 = rank2.text  # 티어표시 (브론즈1,2,3,4,5 등등)
        print(rank4)
        if rank4 != 'Unranked':
          jumsu1 = rank1.find("div", {"class": "TierInfo"})
          jumsu2 = jumsu1.find("span", {"class": "LeaguePoints"})
          jumsu3 = jumsu2.text
          jumsu4 = jumsu3.strip()#점수표시 (11LP등등)
          print(jumsu4)

          winlose1 = jumsu1.find("span", {"class": "WinLose"})
          winlose2 = winlose1.find("span", {"class": "wins"})
          winlose2_1 = winlose1.find("span", {"class": "losses"})
          winlose2_2 = winlose1.find("span", {"class": "winratio"})

          winlose2txt = winlose2.text
          winlose2_1txt = winlose2_1.text
          winlose2_2txt = winlose2_2.text #승,패,승률 나타냄  200W 150L Win Ratio 55% 등등

          print(winlose2txt + " " + winlose2_1txt + " " + winlose2_2txt)

        channel = message.channel
        embed = discord.Embed(
            title='롤'+name+' 전적',
            description=name+'님의 전적입니다.',
            colour=discord.Colour.green()
        )
        if rank4=='Unranked':
            embed.add_field(name='당신의 티어', value=rank4, inline=False)
            embed.add_field(name='-당신은 언랭-', value="언랭은 더이상의 정보가 없습니다.", inline=False)
            await client.send_message(channel, embed=embed)
        else:
         embed.add_field(name='티어', value=rank4, inline=False)
         embed.add_field(name='LP(점수)', value=jumsu4, inline=False)
         embed.add_field(name='승,패 정보', value=winlose2txt+" "+winlose2_1txt, inline=False)
         embed.add_field(name='승률', value=winlose2_2txt, inline=False)
         await client.send_message(channel, embed=embed)
         
            
    if message.content.startswith("레식"):

        learn1 = message.content.split(" ")
        learn = learn1[1]
        name = learn
        enc_name = urllib.parse.quote(name)
        url = "https://r6.tracker.network/profile/pc/"+enc_name
        html = requests.get(url)
        bs = BeautifulSoup(html.text, "html.parser")
        bs_value = bs.find_all("div",{"class": "trn-defstat__value"})
        
        embed = discord.Embed(
            title=learn+ '님 레인보우 식스 전적',
            description=learn,
            colour=discord.Colour.gold()
        )
    
        lvl1 = bs_value[0]
        lvl2 = lvl1.text
        print(lvl2)
        embed.add_field(name='레벨', value=lvl2 , inline=False)

        high_mmr1 = bs_value[1]
        high_mmr2 = high_mmr1.text
        print(high_mmr2)
        embed.add_field(name='최고 MMR', value=high_mmr2, inline=False)

        rank = bs_value[2]
        rank = rank.text
        print(rank)
        embed.add_field(name='현재 랭크', value=rank, inline=False)

        topop1 = bs_value[4]
        print(topop1)

        pvpwin1 = bs_value[5]
        pvpwin2 = pvpwin1.text
        print(pvpwin2)
        embed.add_field(name='PvP 승리', value=pvpwin2, inline=False)

        winratio1 = bs_value[6]
        winratio2 = winratio1.text
        print(winratio2)
        embed.add_field(name='승률', value=winratio2, inline=False)

        pvpkill1 = bs_value[7]
        pvpkill2 = pvpkill1.text
        print(pvpkill2)
        embed.add_field(name='PvP 킬', value=pvpkill2 , inline=False)

        pvpkd1 = bs_value[8]
        pvpkd2 = pvpkd1.text
        print(pvpkd2)
        embed.add_field(name='PvP K/D', value=pvpkd2, inline=False)

        time1 = bs_value[11]
        time2 = time1.text
        print(time2)
        embed.add_field(name='플레이타임', value=time2, inline=False)
        await client.send_message(channel, embed=embed)

    if message.content.startswith("!오퍼"):
        learn1 = message.content.split(" ")
        name = learn1[1]
        op1 = learn1[2]
        op = op1.upper()
        
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

        embed = discord.Embed(
            title=name+ '님 '+op+' 전적',
            description=name,
            colour=discord.Colour.gold()
        )
    
        n1 = name1[i].text
        print(n1)
        embed.add_field(name='오퍼', value=n1 , inline=False)

        j = (i-19)*12

        time = n[j].text
        print(time)
        embed.add_field(name='플레이타임', value=time , inline=False)

        kills = n[j+1].text
        print(kills)
        embed.add_field(name='킬', value=kills , inline=False)

        death = n[j+2].text
        print(death)
        embed.add_field(name='데스', value=death , inline=False)

        kd = n[j+4].text
        print(kd)
        embed.add_field(name='K/D', value=kd , inline=False)

        win = n[j+5].text
        print(win)
        embed.add_field(name='승리', value=win , inline=False)

        lose = n[j+6].text
        print(lose)
        embed.add_field(name='패배', value=lose , inline=False)

        winper = n[j+7].text
        print(winper)
        embed.add_field(name='승률', value=winper , inline=False)

        melee = n[j+8].text
        print(melee)
        embed.add_field(name='근접', value=melee , inline=False)

        head = n[j+9].text
        print(head)
        embed.add_field(name='헤드', value=head , inline=False)

        dbno = n[j+10].text
        print(dbno)
        embed.add_field(name='부상', value=dbno , inline=False)

        xp = n[j+11].text
        print(xp)
        embed.add_field(name='경험치', value=xp , inline=False)

        opstat = n[j+12].text
        print(opstat)
        embed.add_field(name='오퍼 스탯', value=opstat , inline=False)

        await client.send_message(channel, embed=embed)
        
        
    
                 
    if message.content.startswith("버스"):

        learn1 = message.content.split(" ")
        station = learn1[1]
        key = "0XeO7nbthbiRoMUkYGGah20%2BfXizwc0A6BfjrkL6qhh2%2Fsl8j9PzfSLGKnqR%2F1v%2F%2B6AunxntpLfoB3Ryd3OInQ%3D%3D"
        url = "http://61.43.246.153/openapi-data/service/busanBIMS2/stopArr?serviceKey="+key+"&bstopid="+stid(station, 1)
        url1 = "http://61.43.246.153/openapi-data/service/busanBIMS2/stopArr?serviceKey="+key+"&bstopid="+stid(station, 2)
    
        inf1 = urllib.request.urlopen(url)
        info1 = BeautifulSoup(inf1, "html.parser")

        embed = discord.Embed(
            title=station+ '역 버스 도착 정보 1',
            description=station,
            colour=discord.Colour.gold()
        )

        print("*"*20)
    
        for item in info1.findAll('item'):
        
            min1 = ""
            station1=""
            nextstop2 = ""
            no = ""

            if item.arsno == None:
                no = "정보가 없습니다."
            else:
                no = item.arsno.string

            lineno = item.lineno.string
            nextstop1 = nextstop(no, lineno)

            if item.min1 == None:
                min1 = "정보가 없습니다."
            else:
                min1 = item.min1.string

            if item.station1 == None:
            
                station1 = "정보가 없습니다."
            else:
                station1 = item.station1.string

            if nextstop1 == None:
            
                nextstop2 = "정보가 없습니다."

            else:
                nextstop2 = nextstop1
        
            print("버스 번호:",lineno)
            embed.add_field(name='버스 번호', value=lineno , inline=False)
            print("도착 시간:",min1)
            embed.add_field(name='도착 예정 시간', value=min1 , inline=False)
            print("남은 정류소 수:",station1)
            embed.add_field(name='남은 정류소 수', value=station1 , inline=False)
            print("다음 정류장: ", nextstop2)
            embed.add_field(name='다음 정류장', value=nextstop2 , inline=False)
            print("*"*20)

        await client.send_message(channel, embed=embed)

        embed = discord.Embed(
            title=station+ '역 버스 도착 정보 2',
            description=station,
            colour=discord.Colour.gold()
        )

        inf2 = urllib.request.urlopen(url1)
        info2 = BeautifulSoup(inf2, "html.parser")

        print("="*30)
        print("*"*20)

        for item in info2.findAll('item'):
        
            min1 = ""
            station1=""
            nextstop2 = ""
            no = ""

            if item.arsno == None:
                no = "정보가 없습니다."
            else:
                no = item.arsno.string

            lineno = item.lineno.string
            nextstop1 = nextstop(no, lineno)

            if item.min1 == None:
                min1 = "정보가 없습니다."
            else:
                min1 = item.min1.string

            if item.station1 == None:
            
                station1 = "정보가 없습니다."
            else:
                station1 = item.station1.string

            if nextstop1 == None:
            
                nextstop2 = "정보가 없습니다."

            else:
                nextstop2 = nextstop1

            print("버스 번호:",lineno)
            embed.add_field(name='버스 번호', value=lineno , inline=False)
            print("도착 시간:",min1)
            embed.add_field(name='도착 예정 시간', value=min1 , inline=False)
            print("남은 정류소 수:",station1)
            embed.add_field(name='남은 정류소 수', value=station1 , inline=False)
            print("다음 정류장: ", nextstop2)
            embed.add_field(name='다음 정류장', value=nextstop2 , inline=False)
            print("*"*20)

        await client.send_message(channel, embed=embed)

@client.event
async def on_reaction_add(reaction, user):
    
    channel = client.get_channel('579305105107714057')
    
    if reaction.emoji == "\U0001F44C":
        role = discord.utils.get(user.server.roles, id="558210825555410972")
        await client.add_roles(user, role)

@client.event
async def on_reaction_remove(reaction, user):
    if reaction.emoji == "\U0001F44C":
        role = discord.utils.get(user.server.roles, id="558210825555410972")
        await client.remove_roles(user, role)
        
@client.event
async def on_member_join(member):
    fmt = '{1.name} 에 오신것을 환영합니다., {0.mention} 님'
    channel = member.server.get_channel("general")
    await client.send_message(channel, fmt.format(member, member.server))
    await client.send_message(member, "반갑습니다 <@"+id+">님. Lv.75 Bot을 이용해주셔서 감사합니다. 공지를 읽어주기 바랍니다.")

@client.event
async def on_member_remove(member):
    channel = member.server.get_channel("general")
    fmt = '{0.mention} 님이 나갔습니다.'
    await client.send_message(channel, fmt.format(member, member.server))

client.run(token)
