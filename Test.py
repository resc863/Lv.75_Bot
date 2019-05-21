import requests, re
import parser
import urllib
from bs4 import BeautifulSoup
import youtube_dl

opts = {}
with youtube_dl.YoutubeDL(opts) as ydl:
    song_info = ydl.extract_info('https://www.youtube.com/watch?v=dQw4w9WgXcQ', download=False)
    print(song_info)

def get_info():
    name = learn
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

@client.event
async def on_ready():
    Channel = client.get_channel('role_assignment')
    Text= "공지를 읽어주시고 아래 반응을 눌러주세요."
    Moji = await client.send_message(Channel, Text)
    await client.add_reaction(Moji, emoji=':on_hand:')
@client.event
async def on_reaction_add(reaction, user):
    Channel = client.get_channel('role_assignment')
    if reaction.message.channel.id != Channel
    return
    if reaction.emoji == ":on_hand:":
      Role = discord.utils.get(user.server.roles, name="Lv.1 Crook")
      await client.add_roles(user, Role)
learn = "Lv.99_B0SS"
get_info()
