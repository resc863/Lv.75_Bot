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

def check_queue(id)
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
    role = discord.utils.get(discord.server.roles, name="Lv.1 Crook")
    message = await client.send_message(channel, "다음 이모지를 누르세요...")
    while True:
        reaction = await client.wait_for_reaction(emoji="\U0001F44C",message=message)
        await client.add_roles(reaction.message.author, role)
    
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
         
    if message.content.startswith("배그 솔로"):

        learn = message.content.split(" ")
        location = learn[1]
        enc_location = urllib.parse.quote(location)
        url = "https://dak.gg/profile/"+enc_location
        html = requests.get(url)
        bsObj = bs4.BeautifulSoup(html, "html.parser")
        solo1 = bsObj.find("div", {"class": "overview"})
        solo2 = solo1.text
        solo3 = solo2.strip()
        channel = message.channel
        embed = discord.Embed(
            title='배그솔로 정보',
            description='배그솔로 정보입니다.',
            colour=discord.Colour.green())
        if solo3 == "No record":
            print("솔로 경기가 없습니다.")
            embed.add_field(name='배그를 한판이라도 해주세요', value='솔로 경기 전적이 없습니다..', inline=False)
            await client.send_message(channel, embed=embed)

        else:
            solo4 = solo1.find("span", {"class": "value"})
            soloratting = solo4.text  # -------솔로레이팅---------
            solorank0_1 = solo1.find("div", {"class": "grade-info"})
            solorank0_2 = solorank0_1.text
            solorank = solorank0_2.strip()  # -------랭크(그마,브론즈)---------

            print("레이팅 : " + soloratting)
            print("등급 : " + solorank)
            print("")
            embed.add_field(name='레이팅', value=soloratting, inline=False)
            embed.add_field(name='등급', value=solorank, inline=False)

            soloKD1 = bsObj.find("div", {"class": "kd stats-item stats-top-graph"})
            soloKD2 = soloKD1.find("p", {"class": "value"})
            soloKD3 = soloKD2.text
            soloKD = soloKD3.strip()  # -------킬뎃(2.0---------
            soloSky1 = soloKD1.find("span", {"class": "top"})
            soloSky2 = soloSky1.text  # -------상위10.24%---------

            print("킬뎃 : " + soloKD)
            print("킬뎃상위 : " + soloSky2)
            print("")
            embed.add_field(name='킬뎃,킬뎃상위', value=soloKD+" "+soloSky2, inline=False)
            #embed.add_field(name='킬뎃상위', value=soloSky2, inline=False)

            soloWinRat1 = bsObj.find("div", {"class": "stats"})  # 박스
            soloWinRat2 = soloWinRat1.find("div", {"class": "winratio stats-item stats-top-graph"})
            soloWinRat3 = soloWinRat2.find("p", {"class": "value"})
            soloWinRat = soloWinRat3.text.strip()  # -------승률---------
            soloWinRatSky1 = soloWinRat2.find("span", {"class": "top"})
            soloWinRatSky = soloWinRatSky1.text.strip()  # -------상위?%---------

            print("승률 : " + soloWinRat)
            print("승률상위 : " + soloWinRatSky)
            print("")
            embed.add_field(name='승률,승률상위', value=soloWinRat+" "+soloWinRatSky, inline=False)
            #embed.add_field(name='승률상위', value=soloWinRatSky, inline=False)

            soloHead1 = soloWinRat1.find("div", {"class": "headshots stats-item stats-top-graph"})
            soloHead2 = soloHead1.find("p", {"class": "value"})
            soloHead = soloHead2.text.strip()  # -------헤드샷---------
            soloHeadSky1 = soloHead1.find("span", {"class": "top"})
            soloHeadSky = soloHeadSky1.text.strip()  # # -------상위?%---------

            print("헤드샷 : " + soloHead)
            print("헤드샷상위 : " + soloHeadSky)
            print("")
            embed.add_field(name='헤드샷,헤드샷상위', value=soloHead+" "+soloHeadSky, inline=False)
            #embed.add_field(name='헤드샷상위', value=soloHeadSky, inline=False)
            await client.send_message(channel, embed=embed)

    if message.content.startswith("배그 듀오"):

        learn = message.content.split(" ")
        location = learn[1]
        enc_location = urllib.parse.quote(location)
        url = "https://dak.gg/profile/" + enc_location
        html = urllib.request.urlopen(url)
        bsObj = bs4.BeautifulSoup(html, "html.parser")
        duoCenter1 = bsObj.find("section", {"class": "duo modeItem"})
        duoRecord1 = duoCenter1.find("div", {"class": "overview"})
        duoRecord = duoRecord1.text.strip()  # ----기록이없습니다 문구----
        print(duoRecord)
        channel = message.channel
        embed = discord.Embed(
            title='배그듀오 정보',
            description='배그듀오 정보입니다.',
            colour=discord.Colour.green())
        if duoRecord == 'No record':
            print('듀오 경기가 없습니다.')
            embed.add_field(name='배그를 한판이라도 해주세요', value='듀오 경기 전적이 없습니다..', inline=False)
            await client.send_message(channel, embed=embed)

        else:
            duoRat1 = duoRecord1.find("span", {"class": "value"})
            duoRat = duoRat1.text.strip()  # ----레이팅----
            duoRank1 = duoRecord1.find("p", {"class": "grade-name"})
            duoRank = duoRank1.text.strip()  # ----등급----
            print(duoRank)
            embed.add_field(name='레이팅', value=duoRat, inline=False)
            embed.add_field(name='등급', value=duoRank, inline=False)


            duoStat = duoCenter1.find("div", {"class": "stats"})

            duoKD1 = duoStat.find("div", {"class": "kd stats-item stats-top-graph"})
            duoKD2 = duoKD1.find("p", {"class": "value"})
            duoKD = duoKD2.text.strip()  # ----킬뎃----
            duoKdSky1 = duoStat.find("span", {"class": "top"})
            duoKdSky = duoKdSky1.text.strip()  # ----킬뎃 상위?%----
            print(duoKD)
            print(duoKdSky)
            embed.add_field(name='킬뎃,킬뎃상위', value=duoKD+" "+duoKdSky, inline=False)

            duoWinRat1 = duoStat.find("div", {"class": "winratio stats-item stats-top-graph"})
            duoWinRat2 = duoWinRat1.find("p", {"class": "value"})
            duoWinRat = duoWinRat2.text.strip()  # ----승률----
            duoWinRatSky1 = duoWinRat1.find("span", {"class": "top"})
            duoWinRatSky = duoWinRatSky1.text.strip()  # ----승률 상위?%----
            print(duoWinRat)
            print(duoWinRatSky)
            embed.add_field(name='승률,승률상위', value=duoWinRat + " " + duoWinRatSky, inline=False)

            duoHead1 = duoStat.find("div", {"class": "headshots"})
            duoHead2 = duoHead1.find("p", {"class": "value"})
            duoHead = duoHead2.text.strip()  # ----헤드샷----
            duoHeadSky1 = duoHead1.find("span", {"class": "top"})
            duoHeadSky = duoHeadSky1.text.strip()  # ----헤드샷 상위?%----
            print(duoHead)
            print(duoHeadSky)
            embed.add_field(name='헤드샷,헤드샷상위', value=duoHead + " " + duoHeadSky, inline=False)
            await client.send_message(channel, embed=embed)


    if message.content.startswith("배그 스쿼드"):

        learn = message.content.split(" ")
        location = learn[1]
        enc_location = urllib.parse.quote(location)
        url = "https://dak.gg/profile/" + enc_location
        html = urllib.request.urlopen(url)
        bsObj = bs4.BeautifulSoup(html, "html.parser")
        duoCenter1 = bsObj.find("section", {"class": "squad modeItem"})
        duoRecord1 = duoCenter1.find("div", {"class": "overview"})
        duoRecord = duoRecord1.text.strip()  # ----기록이없습니다 문구----
        print(duoRecord)
        channel = message.channel
        embed = discord.Embed(
            title='배그스쿼드 정보',
            description='배그스쿼드 정보입니다.',
            colour=discord.Colour.green())
        if duoRecord == 'No record':
            print('스쿼드 경기가 없습니다.')
            embed.add_field(name='배그를 한판이라도 해주세요', value='스쿼드 경기 전적이 없습니다..', inline=False)
            await client.send_message(channel, embed=embed)

        else:
            duoRat1 = duoRecord1.find("span", {"class": "value"})
            duoRat = duoRat1.text.strip()  # ----레이팅----
            duoRank1 = duoRecord1.find("p", {"class": "grade-name"})
            duoRank = duoRank1.text.strip()  # ----등급----
            print(duoRank)
            embed.add_field(name='레이팅', value=duoRat, inline=False)
            embed.add_field(name='등급', value=duoRank, inline=False)


            duoStat = duoCenter1.find("div", {"class": "stats"})

            duoKD1 = duoStat.find("div", {"class": "kd stats-item stats-top-graph"})
            duoKD2 = duoKD1.find("p", {"class": "value"})
            duoKD = duoKD2.text.strip()  # ----킬뎃----
            duoKdSky1 = duoStat.find("span", {"class": "top"})
            duoKdSky = duoKdSky1.text.strip()  # ----킬뎃 상위?%----
            print(duoKD)
            print(duoKdSky)
            embed.add_field(name='킬뎃,킬뎃상위', value=duoKD+" "+duoKdSky, inline=False)

            duoWinRat1 = duoStat.find("div", {"class": "winratio stats-item stats-top-graph"})
            duoWinRat2 = duoWinRat1.find("p", {"class": "value"})
            duoWinRat = duoWinRat2.text.strip()  # ----승률----
            duoWinRatSky1 = duoWinRat1.find("span", {"class": "top"})
            duoWinRatSky = duoWinRatSky1.text.strip()  # ----승률 상위?%----
            print(duoWinRat)
            print(duoWinRatSky)
            embed.add_field(name='승률,승률상위', value=duoWinRat + " " + duoWinRatSky, inline=False)

            duoHead1 = duoStat.find("div", {"class": "headshots"})
            duoHead2 = duoHead1.find("p", {"class": "value"})
            duoHead = duoHead2.text.strip()  # ----헤드샷----
            duoHeadSky1 = duoHead1.find("span", {"class": "top"})
            duoHeadSky = duoHeadSky1.text.strip()  # ----헤드샷 상위?%----
            print(duoHead)
            print(duoHeadSky)
            embed.add_field(name='헤드샷,헤드샷상위', value=duoHead + " " + duoHeadSky, inline=False)
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
        
    if message.content.startswith("!연결"):
        channel = message.author.voice.voice_channel
        server = message.server
        voice_client = client.voice_client_in(server)
        print(voice_client)
        
        if voice_client== None:
            await client.send_message(message.channel, '들어왔습니다') # 호오.... 나를 부르는건가? 네녀석.. 각오는 되있겠지?
            await client.join_voice_channel(channel)
        else:
            await client.send_message(message.channel, '봇이 이미 들어와있습니다.') # 응 이미 들어와있어 응쓰게싸

    if message.content.startswith("!종료"):
        server = message.server
        voice_client = client.voice_client_in(server)
            
        if voice_client == None:
            await client.send_message(message.channel,'봇이 음성채널에 접속하지 않았습니다.') # 원래나가있었음 바보녀석 니녀석의 죄는 "어리석음" 이라는 .것.이.다.
            pass
        else:
            await client.send_message(message.channel, '나갑니다') # 나가드림
            await voice_client.disconnect()


    if message.content.startswith("!play"):
        
        channel = message.author.voice.voice_channel
        server = message.server
        voice_client = client.voice_client_in(server)
        print(voice_client)
        
        if voice_client== None:
            await client.join_voice_channel(channel)

        voice_client = client.voice_client_in(server)

        msg1 = message.content.split(" ")
        url = msg1[1]
        player = await voice_client.create_ytdl_player(url, after=lambda: check_queue(server.id))
        print(player.is_playing())
        players[server.id] = player
        await client.send_message(message.channel, embed=discord.Embed(description="재생"))
        print(player.is_playing())
        player.start()


    if message.content.startswith("!pause"):
        id = message.server.id
        await client.send_message(message.channel, embed=discord.Embed(description="장비를 정지합니다"))
        players[id].pause()

    if message.content.startswith("!rep"):
        id = message.server.id
        await client.send_message(message.channel, embed=discord.Embed(description="다시재생"))
        players[id].resume()

    if message.content.startswith("!stop"):
        id = message.server.id
        await client.send_message(message.channel, embed=discord.Embed(description="정지"))
        players[id].stop()
        print(players[id].is_playing())

    if message.content.startswith('!add'):
        msg1 = message.content.split(" ")
        url = msg1[1]
        server = message.server
        voice_client = client.voice_client_in(server)
        player = await voice_client.create_ytdl_player(url, after=lambda: check_queue(server.id))
        print(player)

        if server.id in queues:
            queues[server.id].append(player)
            print('if 1 '+str(queues[server.id])) #queues배열 확인
        else:
            queues[server.id] = [player] #딕셔너리 쌍 추가
            print('else 1' + str(queues[server.id]))#queues배열 확인
        await client.send_message(message.channel,'예약 완료\n')
        musiclist.append(url) #대기목록 링크


    if message.content.startswith('!list'):

        server = message.server
        msg1 = message.content.split(" ")
        mList = msg1[1]
        num = 0
        bSize = len(musiclist)

        if mList =='w':
            embed = discord.Embed(
                title='대기중인 곡 들',
                description='대기중.....',
                colour=discord.Colour.blue()
            )
            for i in musiclist:
                print('예약리스트 : ' + i)
                embed.add_field(name='대기중인 곡', value=i, inline=False)
            await client.send_message(message.channel, embed=embed)

        if mList =='c':
            while num<bSize:
                del musiclist[0]
                num = num+1

            del queues[server.id]
            await client.send_message(message.channel,'예약중인 음악 모두 취소 완료')

        
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
