import json
import discord
from discord.ext import commands, tasks
from util import countdownEmbeds, countdowns, updateFiles
from discord.ext.commands import CommandNotFound

client = commands.Bot(command_prefix="$", help_command=None)
f = open("token.txt", "r")
TOKEN = f.read()

countdown_title = ''
countdown_description = ''
countdown_time = ''
countdown_image = ''
countdown_thumbnail = ''
countdown_msg = ''
countdown_mention = ''
countdown_author_name = ''
countdown_author_icon = ''
countdown_announcement_channel = 'countdown-announcements'


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
    global countdown_announcement_channel
    countdown_announcement_channel = 'countdown-announcements'


def add_server(guildID):
    # open orig file as dict
    path = 'util/countdown-data.json'
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
    # inform when bot code is running
    print('We have logged in as {0.user}'.format(client))
    # start the task.loop
    update.start()


@client.event
async def on_guild_join(guild):
    # call method to add a new server to countdown-data.json
    add_server(str(guild.id))


@tasks.loop(seconds=1)
async def update():
    # load json file to a dict
    path = 'util/countdown-data.json'
    with open(path, 'r') as f:
        data = json.load(f)
    # for each messageID in each guildID, update the countdown
    for x in client.guilds:
        for y in data[str(x.id)]:
            await countdowns.update_countdown(x, y)


@tasks.loop(seconds=86400)
async def reset_channel():
    for x in client.guilds:
        existing_channel = discord.utils.get(x.channels, name='countdown')
        if existing_channel is not None:
            try:
                await existing_channel.purge(limit=20)
                # clears the channel to remove messages
            except Exception as e:
                print("Error in purging messages")


@client.command()
async def countdown(ctx):
    # checks to see if time is empty
    if countdown_time == '':
        await ctx.send("Please enter a time!")
    # if not empty
    else:
        try:
            # check to see if time has already passed
            not_valid_time = countdowns.check_time_validity(countdown_time)
            if not_valid_time:
                await ctx.send("Please check your time, you may be entering a time that has already passed!")
            else:
                # add countdown to json file so task.loop can update it
                updateFiles.write_file(ctx.guild.id)
        except ValueError as e:  # catch any other errors
            print(e)
            await ctx.send("Please check your values, something went wrong!")
            return


@client.command()
async def new(ctx):
    # resets all the values
    set_embed_values()
    await ctx.send("Create new countdown!")
    updateFiles.write_temp(countdown_title, countdown_description, countdown_time, countdown_image,
                           countdown_thumbnail, countdown_msg, countdown_mention,
                           countdown_author_name, countdown_author_icon, countdown_announcement_channel)


@client.command()
async def stop(ctx, messageID):  # stop using the command and the messageID
    guildID = ctx.guild.id
    # turn json file to dict
    path = 'util/countdown-data.json'
    with open(path, 'r') as f:
        data = json.load(f)
    # get the channel to delete the specific message
    cd_channel = discord.utils.get(ctx.guild.channels, name='countdown')
    message_to_delete = await cd_channel.fetch_message(messageID)
    await message_to_delete.delete()
    del data[str(guildID)][str(messageID)]
    # update json file
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)
    await ctx.send("Stopped Timer!")


@client.command()
async def help(ctx):
    # call the method to send help embed
    helpEmbed = countdownEmbeds.help_embed()
    await ctx.send(embed=helpEmbed)


@client.event
async def on_message(command):
    # makes sure its not a command
    await client.process_commands(command)
    # global variables
    global countdown_title, countdown_description, countdown_time, countdown_image, \
        countdown_thumbnail, countdown_msg, countdown_mention, countdown_author_name, \
        countdown_author_icon, countdown_announcement_channel
    cmd = command.content.lower()
    message_set = False
    message_edit = False
    guildid = command.guild.id
    countdown_id = ''
    # if message is an edit
    if cmd.startswith("edit"):
        path = 'util/countdown-data.json'
        with open(path, 'r') as f:
            data = json.load(f)
        # break down the message into the word edit, messageID, the specific part of the embed to change, and the value
        list_of_words = cmd.split(" ")
        joined_values = " ".join(list_of_words[3:])
        countdown_id = list_of_words[1]
        part_to_change = list_of_words[2]
        for countdown_messages in data[str(guildid)]:
            # if countdown_id exists in the json file
            if countdown_id == countdown_messages:
                # directly update the file instead of storing and updating later
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
                    # for specific person, kinda not ideal way but it will do
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
    # if setting initial values
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
    elif cmd.startswith("set channel "):
        countdown_announcement_channel = command.content[12:]
        message_set = True
    elif cmd.startswith("set mention "):
        if command.content[12:].lower() == "me":
            author = "Countdown Buddy will ping " + f"{command.author.mention} when countdown ends!"
            await command.channel.send(author)
            countdown_mention = command.author.mention
            countdown_author_name = command.author.name
            countdown_author_icon = str(command.author.avatar_url)[35:]
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
    # run if its a set countdown
    if message_set:
        updateFiles.write_temp(countdown_title, countdown_description, countdown_time, countdown_image,
                               countdown_thumbnail, countdown_msg, countdown_mention,
                               countdown_author_name, countdown_author_icon, countdown_announcement_channel)
        new_embed = countdownEmbeds.details_embed()
        await command.channel.send(embed=new_embed)
    # run if its a message edit
    elif message_edit:
        new_embed = countdownEmbeds.edit_details_embed(guildid, countdown_id)
        await command.channel.send(embed=new_embed)


# any other errors
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return
    raise error


client.run(TOKEN)
