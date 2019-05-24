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
async def on_member_join(member):
    fmt = '{1.name} 에 오신것을 환영합니다., {0.mention} 님. '
    channel = member.server.get_channel("chat")
    await client.send_message(channel, fmt.format(member, member.server))
    await client.send_message(member, "반갑습니다. <@"+id+">님.")
    role = discord.utils.get(member.server.roles, name="<[Guest]>")
    await client.add_roles(member, role)

client.run(token)
