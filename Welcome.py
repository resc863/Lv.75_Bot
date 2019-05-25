import discord
import asyncio
import os
import sys
from discord import Member
from discord.ext import commands

client = discord.Client()
token = os.environ["key"]

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
    channel = member.server.get_channel("450316317988356100")
    role = discord.utils.get(member.server.roles, id="450322259660374036")
    await client.send_message(channel, fmt.format(member, member.server))
    await client.send_message(member, "반갑습니다.")
    await client.add_roles(member, role)

client.run(token)
