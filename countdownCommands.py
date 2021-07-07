import asyncio
import json
import discord
from discord.ext import commands, tasks
from datetime import timedelta, datetime
import countdownEmbeds
import updateFiles
import countdowns

client = commands.Bot(command_prefix="$", help_command=None)
f = open("token.txt", "r")
TOKEN = f.read()

# Things to do:
# Create timer for each individual countdown
# Have a method that calls each one and runs it
# Access each countdown in tasks.loop

countdown_title = ''
countdown_description = ''
countdown_time = ''
countdown_image = ''
countdown_thumbnail = ''
countdown_msg = ''
countdown_mention = ''
countdown_author_name = ''
countdown_author_icon = ''


# def get_countdowns():


def set_embed_values():
    global countdown_title
    countdown_title = ''
    global countdown_description
    countdown_description = ''
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
    global countdown_author_name
    countdown_author_name = ''
    global countdown_author_icon
    countdown_author_icon = ''


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


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    # countdowns.check_expiry(client)
    update.start()


@client.event
async def on_guild_join(guild):
    add_server(str(guild.id))


@tasks.loop(seconds=1)
async def update():
    path = 'countdown-data.json'
    with open(path, 'r') as f:
        data = json.load(f)

    for x in client.guilds:
        for y in data[str(x.id)]:
            await countdowns.update_countdown(x, y)
    # new_message = countdownEmbeds.new_msg(endtime="2021-06-28 15:00:00")
    # await embeds.update_msg(new_message, msg)


@client.command()
async def countdown(ctx):
    if countdown_time == '':
        await ctx.send("Dude give me a time wth")
    try:
        message = await countdownEmbeds.new_msg(ctx, countdown_time)
        updateFiles.write_file(ctx.guild.id)
    except ValueError as e:
        print(e)
        await ctx.send("Please check your time values, something went wrong!")
        return


@client.command()
async def new(ctx):
    set_embed_values()
    await ctx.send("Create new countdown!")
    updateFiles.write_temp(countdown_title, countdown_description, countdown_time, countdown_image,
                           countdown_thumbnail, countdown_msg, countdown_mention,
                           countdown_author_name, countdown_author_icon)

@client.event
async def on_message(command):
    await client.process_commands(command)
    global countdown_title, countdown_description, countdown_time, countdown_image, \
        countdown_thumbnail, countdown_msg, countdown_mention, countdown_author_name, countdown_author_icon
    cmd = command.content.lower()
    message_set = False
    message_edit = False
    if cmd.startswith("edit"):
        path = 'countdown-data.json'
        with open(path, 'r') as f:
            data = json.load(f)

        list_of_words = cmd.split(" ")
        joined_values = " ".join(list_of_words[3:])
        print(joined_values)
        countdown_id = list_of_words[1]
        part_to_change = list_of_words[2]
        guildid = command.guild.id
        for countdown_messages in data[str(guildid)]:
            if countdown_id == countdown_messages:
                if part_to_change == "title":
                    data[str(guildid)][str(countdown_id)]['Title'] = joined_values
                    message_edit = True
                elif part_to_change == "description":
                    data[str(guildid)][str(countdown_id)]['Description'] = joined_values
                    message_edit = True
                elif part_to_change == "time":
                    data[str(guildid)][str(countdown_id)]['Field Value'] = joined_values
                    message_edit = True
                elif part_to_change == "image":
                    data[str(guildid)][str(countdown_id)]['Image'] = joined_values
                    message_edit = True
                elif part_to_change == "thumbnail":
                    data[str(guildid)][str(countdown_id)]['Thumbnail'] = joined_values
                    message_edit = True
                elif part_to_change == "message":
                    data[str(guildid)][str(countdown_id)]['Message'] = joined_values
                    message_edit = True
                elif part_to_change == "mention":
                    if joined_values == "me":
                        author = "Countdown Buddy will ping " + f"{command.author.mention} when countdown ends!"
                        await command.channel.send(author)
                        data[str(guildid)][str(countdown_id)]['Mention'] = command.author.mention
                        countdown_author_name = command.author.name
                        countdown_author_icon = str(command.author.avatar_url)[35:]
                        message_edit = True
                    elif joined_values == "here":
                        await command.channel.send("Countdown Buddy will ping ``@here`` when countdown ends!")
                        data[str(guildid)][str(countdown_id)]['Mention'] = joined_values
                        message_edit = True
                    elif joined_values == "everyone":
                        await command.channel.send("Countdown Buddy will ping ``@everyone`` when countdown ends!")
                        data[str(guildid)][str(countdown_id)]['Mention'] = joined_values
                        message_edit = True
                    elif joined_values.startswith("<@!") and joined_values.endswith(">"):
                        userid = joined_values
                        userid = userid.replace("<", "")
                        userid = userid.replace(">", "")
                        userid = userid.replace("@", "")
                        user = "Countdown Buddy will ping " + f"<@{userid}> when countdown ends!"
                        await command.channel.send(user)
                        data[str(guildid)][str(countdown_id)]['Mention'] = joined_values
                        message_edit = True
        with open(path, 'w') as f:
            json.dump(data, f, indent=4)

    elif cmd.startswith("set title "):
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
        if command.content[12:].lower() == "me":
            author = "Countdown Buddy will ping " + f"{command.author.mention} when countdown ends!"
            await command.channel.send(author)
            countdown_mention = command.author.mention
            countdown_author_name = command.author.name
            countdown_author_icon = str(command.author.avatar_url)[35:]
            # print(countdown_author_name)
            # print(countdown_author_icon)
            message_set = True
        elif command.content[12:].lower() == "here":
            await command.channel.send("Countdown Buddy will ping ``@here`` when countdown ends!")
            countdown_mention = command.content[12:]
            message_set = True
        elif command.content[12:].lower() == "everyone":
            await command.channel.send("Countdown Buddy will ping ``@everyone`` when countdown ends!")
            countdown_mention = command.content[12:]
            message_set = True
        elif command.content[12:].lower().startswith("<@!") and command.content[12:].lower().endswith(">"):
            userid = command.content[12:].lower()
            userid = userid.replace("<", "")
            userid = userid.replace(">", "")
            userid = userid.replace("@", "")
            user = "Countdown Buddy will ping " + f"<@{userid}> when countdown ends!"
            await command.channel.send(user)
            countdown_mention = command.content[12:]
            message_set = True

    if message_set:
        updateFiles.write_temp(countdown_title, countdown_description, countdown_time, countdown_image,
                               countdown_thumbnail, countdown_msg, countdown_mention,
                               countdown_author_name, countdown_author_icon)
        new_embed = countdownEmbeds.details_embed()
        await command.channel.send(embed=new_embed)


client.run(TOKEN)
