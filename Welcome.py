import discord
import asyncio
from discord import Member
from discord.ext import commands

client = discord.Client()
token = os.environ(key)

@client.event
async def on_ready():
    print("Logged in ") 
    print(client.user.name)
    print(client.user.id)
    print("===============")
    await client.change_presence(game=discord.Game(name=":D", type=1))

@client.event
async def on_reaction_add(reaction, user):
    Channel = client.get_channel('chat')
    if reaction.message.channel.id != Channel
    return
    if reaction.emoji == ":ok_hand:":
      Role = discord.utils.get(user.server.roles, name="[Guest]")
      await client.add_roles(user, Role)

@client.event
async def on_member_join(member):
    fmt = '{1.name} 에 오신것을 환영합니다., {0.mention} 님'
    channel = member.server.get_channel("chat")
    await client.send_message(channel, fmt.format(member, member.server))
    await client.send_message(member, "반갑습니다 <@"+id+">님.")
    Text= "공지를 읽어주시고 아래 반응을 눌러주세요."
    Moji = await client.send_message(channel, Text)
    await client.add_reaction(Moji, emoji=':ok_hand:')



client.run(token)
