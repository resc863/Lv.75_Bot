import discord
import asyncio
import os
import sys
from discord import Member
from discord.ext import commands
from itertools import cycle

client = discord.Client()

token = os.environ["key"]

@client.event
async def on_ready():
    print("Logged in ") 
    print(client.user.name)
    print(client.user.id)
    print("====================")

@client.event
async def on_message(message):
    if message.content.startswith("!역할"):
        
        channel = client.get_channel('592296776850210816')

        embed = discord.Embed(title="레인보우 식스", description="레인보우 식스 관련 역할", color=0x00ff00)
        embed.add_field(name="멘션 허용", value="레인보우 식스 관련 멘션을 받으려면 첫번째 버튼을 누르세요", inline=False)
        embed.add_field(name="멘션 거부", value="레인보우 식스 관련 멘션을 받지 않으려면 두번째 버튼을 누르세요", inline=False)
        message = await client.send_message(channel, embed=embed)
        await client.add_reaction(message, emoji="\U0001F600")
        await client.add_reaction(message, emoji="\U0001F64F")
        
        embed = discord.Embed(title="데스티니 2", description="데스티니 2 관련 역할", color=0x00ff00)
        embed.add_field(name="멘션 허용", value="데스티니 2 관련 멘션을 받으려면 첫번째 버튼을 누르세요", inline=False)
        embed.add_field(name="멘션 거부", value="데스티니 2 관련 멘션을 받지 않으려면 두번째 버튼을 누르세요", inline=False)
        message = await client.send_message(channel, embed=embed)
        await client.add_reaction(message, emoji="\U0001F910")
        await client.add_reaction(message, emoji="\U0001F44F")
        
        embed = discord.Embed(title="GTA5", description="GTA5 관련 역할", color=0x00ff00)
        embed.add_field(name="멘션 허용", value="GTA5 관련 멘션을 받으려면 첫번째 버튼을 누르세요", inline=False)
        embed.add_field(name="멘션 거부", value="GTA5 관련 멘션을 받지 않으려면 두번째 버튼을 누르세요", inline=False)
        message = await client.send_message(channel, embed=embed)
        await client.add_reaction(message, emoji="\U0001F91D")
        await client.add_reaction(message, emoji="\U0001F91A")

        embed = discord.Embed(title="마인크래프트", description="마인크래프트 관련 역할", color=0x00ff00)
        embed.add_field(name="멘션 허용", value="마인크래프트 관련 멘션을 받으려면 첫번째 버튼을 누르세요", inline=False)
        embed.add_field(name="멘션 거부", value="마인크래프트 관련 멘션을 받지 않으려면 두번째 버튼을 누르세요", inline=False)
        message = await client.send_message(channel, embed=embed)
        await client.add_reaction(message, emoji="\U0001F590")
        await client.add_reaction(message, emoji="\U0001F488")

        embed = discord.Embed(title="콜오브듀티", description="콜오브듀티 관련 역할", color=0x00ff00)
        embed.add_field(name="멘션 허용", value="콜오브듀티 관련 멘션을 받으려면 첫번째 버튼을 누르세요", inline=False)
        embed.add_field(name="멘션 거부", value="콜오브듀티 관련 멘션을 받지 않으려면 두번째 버튼을 누르세요", inline=False)
        message = await client.send_message(channel, embed=embed)
        await client.add_reaction(message, emoji="\U0001F5A5")
        await client.add_reaction(message, emoji="\U00002328")

    if message.content.startswith("!가이드"):  
        channel = client.get_channel('638039195234992155')

        embed = discord.Embed(title="[Unknown Company]에 오신 것을 환영합니다!", description="다음을 읽고 버튼을 눌러 주십시오.", color=0x00ff00)
        message = await client.send_message(channel, embed=embed)
        await client.add_reaction(message, emoji="\U0001F446")

@client.event
async def on_reaction_add(reaction, user):

    if reaction.emoji == "\U0001F446":
        role = discord.utils.get(user.server.roles, id="450322259660374036")
        await client.add_roles(user, role)
        
    if reaction.emoji == "\U0001F44F":
        role = discord.utils.get(user.server.roles, id="638038286392098818")
        await client.add_roles(user, role)

    if reaction.emoji == "\U0001F600":
        role = discord.utils.get(user.server.roles, id="592295687786594305")
        await client.add_roles(user, role)

    if reaction.emoji == "\U0001F64F":
        role = discord.utils.get(user.server.roles, id="592296285994745856")
        await client.add_roles(user, role)

    if reaction.emoji == "\U0001F910":
        role = discord.utils.get(user.server.roles, id="638035231349276672")
        await client.add_roles(user, role)
    
    if reaction.emoji == "\U0001F91D":
        role = discord.utils.get(user.server.roles, id="638522416611721216")
        await client.add_roles(user, role)
    
    if reaction.emoji == "\U0001F91A":
        role = discord.utils.get(user.server.roles, id="638038441010921484")
        await client.add_roles(user, role)
    
    if reaction.emoji == "\U0001F590":
        role = discord.utils.get(user.server.roles, id="638036108235636746")
        await client.add_roles(user, role)
    
    if reaction.emoji == "\U0001F488":
        role = discord.utils.get(user.server.roles, id="638038347746377768")
        await client.add_roles(user, role)

    if reaction.emoji == "\U0001F5A5":
        role = discord.utils.get(user.server.roles, id="638035923799375893")
        await client.add_roles(user, role)

    if reaction.emoji == "\U00002328":
        role = discord.utils.get(user.server.roles, id="638038402297626634")
        await client.add_roles(user, role)
        
@client.event
async def on_reaction_remove(reaction, user):

    if reaction.emoji == "\U0001F446":
        role = discord.utils.get(user.server.roles, id="450322259660374036")
        await client.remove_roles(user, role)
        
    if reaction.emoji == "\U0001F44F":
        role = discord.utils.get(user.server.roles, id="638038286392098818")
        await client.remove_roles(user, role)

    if reaction.emoji == "\U0001F600":
        role = discord.utils.get(user.server.roles, id="592295687786594305")
        await client.remove_roles(user, role)

    if reaction.emoji == "\U0001F64F":
        role = discord.utils.get(user.server.roles, id="592296285994745856")
        await client.remove_roles(user, role)

    if reaction.emoji == "\U0001F910":
        role = discord.utils.get(user.server.roles, id="638035231349276672")
        await client.remove_roles(user, role)
    
    if reaction.emoji == "\U0001F91D":
        role = discord.utils.get(user.server.roles, id="638522416611721216")
        await client.remove_roles(user, role)
    
    if reaction.emoji == "\U0001F91A":
        role = discord.utils.get(user.server.roles, id="638038441010921484")
        await client.remove_roles(user, role)
    
    if reaction.emoji == "\U0001F590":
        role = discord.utils.get(user.server.roles, id="638036108235636746")
        await client.remove_roles(user, role)
    
    if reaction.emoji == "\U0001F488":
        role = discord.utils.get(user.server.roles, id="638038347746377768")
        await client.remove_roles(user, role)

    if reaction.emoji == "\U0001F5A5":
        role = discord.utils.get(user.server.roles, id="638035923799375893")
        await client.remove_roles(user, role)

    if reaction.emoji == "\U00002328":
        role = discord.utils.get(user.server.roles, id="638038402297626634")
        await client.remove_roles(user, role)
        
    

client.run(token)
