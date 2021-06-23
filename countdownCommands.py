import asyncio
import json
import discord
from discord.ext import commands, tasks
from datetime import timedelta, datetime
import countdownEmbeds

client = commands.Bot(command_prefix="$", help_command=None)
f = open("token.txt", "r")
TOKEN = f.read()

# Things to do:
# Create timer for each individual countdown
# Have a method that calls each one and runs it
# Access each countdown in tasks.loop

countdown_title = 'cok'
countdown_description = 'nice'
countdown_header = 'Time Remaining: '
countdown_time = '2021-06-28 15:00:00'
countdown_image = ''
countdown_thumbnail = ''
countdown_msg = ''
countdown_mention = ''


# def get_countdowns():


def set_embed_values():
    global countdown_title
    countdown_title = ''
    global countdown_description
    countdown_description = ''
    global countdown_header
    countdown_header = 'Time Remaining:'
    global countdown_time
    countdown_time = ''
    global countdown_image
    countdown_image = ''
    global countdown_thumbnail
    countdown_thumbnail = ''
    global countdown_msg
    countdown_msg = ''
    global countdown_mention
    countdown_mention = ''


@client.event
async def on_message(command):
    await client.process_commands(command)
    global countdown_title, countdown_description, countdown_header, countdown_time, countdown_image, \
        countdown_thumbnail, countdown_msg, countdown_mention
    cmd = command.content.lower()
    message_set = False

    if cmd.startswith("set title "):
        countdown_title = command.content[10:]
        message_set = True
    elif cmd.startswith("set description "):
        countdown_description = command.content[16:]
        message_set = True
    elif cmd.startswith("set time "):
        countdown_time = command.content[9:]
        message_set = True
    elif cmd.startswith("set image "):
        countdown_image = command.content[10:]
        message_set = True
    elif cmd.startswith("set thumbnail "):
        countdown_thumbnail = command.content[14:]
        message_set = True
    elif cmd.startswith("set message "):
        countdown_msg = command.content[12:]
        message_set = True
    elif cmd.startswith("set mention "):
        if command.content[12:].lower() == "creator":
            author = "Countdown Buddy will ping " + f"{command.author.mention} when countdown ends!"
            await command.channel.send(author)
            countdown_mention = command.content[12:]
            message_set = True
        elif command.content[12:].lower() == "here":
            await command.channel.send("Countdown Buddy will ping ``@here`` when countdown ends!")
            countdown_mention = command.content[12:]
            message_set = True
        elif command.content[12:].lower() == "everyone":
            await command.channel.send("Countdown Buddy will ping ``@everyone`` when countdown ends!")
            countdown_mention = command.content[12:]
            message_set = True

    if message_set:
        new_embed = details_embed()
        await command.channel.send(embed=new_embed)


def write_file(guildID):
    path = 'countdown-data.json'
    with open(path, 'r') as f:
        data = json.load(f)
        temp = data[str(guildID)]
        # append new server data to dict
        append = {"temp": {'Title': countdown_title, 'Description': countdown_description, 'Field Name': countdown_header,
                         'Field Value': countdown_time, 'Image': countdown_image, 'Thumbnail': countdown_thumbnail}}
        temp.update(append)
    # write updated dict to file
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)


def write_temp():
    path = 'temp-data.json'
    with open(path, 'r') as f:
        data = json.load(f)
    # append new server data to dict
    append = {'Title': countdown_title, 'Description': countdown_description, 'Field Name': countdown_header,
              'Field Value': countdown_time, 'Image': countdown_image, 'Thumbnail': countdown_thumbnail}
    data.update(append)
    # write updated dict to file
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)


def add_server(guildID):
    # open orig file as dict
    path = 'countdown-data.json'
    with open(path, 'r') as f:
        data = json.load(f)
    # append new server data to dict
    append = {guildID: {}}
    data.update(append)
    # write updated dict to file
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)


async def update_countdown(client, guild, messageID):
    try:
        if discord.utils.get(guild.channels, name='countdown') is None:
            cd_channel = await guild.create_text_channel('countdown')
            await cd_channel.edit(position=0, sync_permissions=True)
        else:
            cd_channel = discord.utils.get(guild.channels, name='countdown')

        path = 'countdown-data.json'
        with open(path, 'r') as f:
            data = json.load(f)

        time = data[str(guild.id)][str(messageID)][str("Field Value")]
        new_time = countdownEmbeds.new_msg(time)
        new_message = countdownEmbeds.set_embed(new_time)
        if messageID == "temp":
            message = await cd_channel.send(embed=new_message)
            append = {str(message.id): {'Title': countdown_title, 'Description': countdown_description, 'Field Name': countdown_header,
                      'Field Value': countdown_time, 'Image': countdown_image, 'Thumbnail': countdown_thumbnail}}
            data[str(guild.id)].update(append)
            del data[str(guild.id)]["temp"]
            with open(path, 'w') as f:
                json.dump(data, f, indent=4)
        else:
            try:
                cd_message = await cd_channel.fetch_message(messageID)
                await cd_message.edit(embed=new_message)
            except Exception as e: #if bot can't edit a message, reset channel and display a new leaderboard
                print(f"leaderboard edit error: {e}")
                delete_message = await cd_channel.fetch_message(messageID)
                await delete_message.delete()
                message = await cd_channel.send(embed=new_message)
                data[str(message.id)] = data[str(messageID)]
                del data[str(messageID)]
                with open(path, 'w') as f:
                    json.dump(data, f, indent=4)
    except Exception as e:
        print(f"leaderboard error in server {guild.name}")
        print(e)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    # new_message = countdownEmbeds.set_embed("pog")
    # channel = client.get_channel(832287981091160105)
    # await channel.send(embed=new_message)
    # channel = client.get_channel(832287981091160105)
    # new_message = countdownEmbeds.new_msg("2021-06-28 15:00:00")
    # msg = await channel.send(new_message)
    # update.start(msg)
    # channel = client.get_channel(832287981091160105)
    # new_message = countdownEmbeds.new_msg("2021-06-28 15:00:00")
    # msg = await channel.send(new_message)
    # update.start(msg)
    update.start("nice")


@client.event
async def on_guild_join(guild):
    add_server(str(guild.id))


@tasks.loop(seconds=1)
async def update(msg):
    path = 'countdown-data.json'
    with open(path, 'r') as f:
        data = json.load(f)

    for x in client.guilds:
        for y in data[str(x.id)]:
            await update_countdown(client, x, y)
    # new_message = countdownEmbeds.new_msg(endtime="2021-06-28 15:00:00")
    # await embeds.update_msg(new_message, msg)


@client.command()
async def countdown(ctx):
    new_message = countdownEmbeds.new_msg(endtime=countdown_time)
    write_file(ctx, message_ID)

write_file("774320079650160640")
write_temp()

client.run(TOKEN)
