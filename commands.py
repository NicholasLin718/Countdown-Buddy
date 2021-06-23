import asyncio
import json
import discord
from discord.ext import commands, tasks
from datetime import timedelta, datetime
import embeds


client = commands.Bot(command_prefix= "$", help_command=None)
f = open("token.txt", "r")
TOKEN = f.read()

#Things to do:
# Create timer for each individual countdown
# Have a method that calls each one and runs it
# Access each countdown in tasks.loop



def get_countdowns():


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    channel = client.get_channel(832287981091160105)
    new_message = embeds.new_msg()
    msg = await channel.send(new_message)
    update.start(msg)


@tasks.loop(seconds=1)
async def update(msg):
    new_message = embeds.new_msg()
    await embeds.update_msg(new_message, msg)

client.run(TOKEN)

