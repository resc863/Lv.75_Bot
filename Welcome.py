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
    Channel = client.get_channel('role_assignment')
    Text= "공지를 읽어주시고 아래 반응을 눌러주세요."
    Moji = await client.send_message(Channel, Text)

@client.event
async def on_reaction_add(reaction, user):
    Channel = client.get_channel('notice')
    if reaction.message.channel.id != Channel
    return
    if reaction.emoji == ":ok_hand:":
      Role = discord.utils.get(user.server.roles, name="[guest]")
      await client.add_roles(user, Role)

client.run(token)
