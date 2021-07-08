import json
from datetime import timedelta, datetime
import discord


async def update_msg(new_message, msg):
    await msg.edit(content=new_message)


async def send_msg(guild, countdown):
    new_message = await guild.send(content=countdown)
    return new_message.id


async def new_msg(ctx, endtime):
    y = int(endtime[0:4])
    mon = int(endtime[5:7])
    d = int(endtime[8:10])
    h = int(endtime[11:13])
    m = int(endtime[14:16])
    s = int(endtime[17:19])
    date_now = datetime.today()
    date_now_timestamp = int(date_now.timestamp())
    last_day_date = datetime(year=y, month=mon, day=d, hour=h, minute=m, second=s)
    last_day_timestamp = int(last_day_date.timestamp())
    remaining_time_seconds = last_day_timestamp - date_now_timestamp

    remaining_time = timedelta(seconds=remaining_time_seconds)
    remaining_days = remaining_time.days
    remaining_seconds = remaining_time.seconds

    remaining_minutes, remaining_seconds = divmod(remaining_seconds, 60)
    remaining_hours, remaining_minutes = divmod(remaining_minutes, 60)
    if date_now_timestamp >= last_day_timestamp:
        message = "Timer has ended."
        return message

    if remaining_days:
        if remaining_days > 1:
            remaining_days = '{} days '.format(remaining_days)
        else:
            remaining_days = '{} day '.format(remaining_days)
    else:
        remaining_days = ''

    if remaining_hours:
        if remaining_hours > 1:
            remaining_hours = '{} hours '.format(remaining_hours)
        else:
            remaining_hours = '{} hour '.format(remaining_hours)
    else:
        remaining_hours = ''

    if remaining_minutes:
        if remaining_minutes > 1:
            remaining_minutes = '{} minutes '.format(remaining_minutes)
        else:
            remaining_minutes = '{} minute '.format(remaining_minutes)
    else:
        remaining_minutes = ''

    if remaining_seconds:
        if remaining_seconds > 1:
            remaining_seconds = '{} seconds '.format(remaining_seconds)
        else:
            remaining_seconds = '{} second '.format(remaining_seconds)
    else:
        remaining_seconds = ''

    message = "{}{}{}{}".format(remaining_days, remaining_hours, remaining_minutes, remaining_seconds)
    return message


def set_temp_embed(message):
    path = 'temp-data.json'
    with open(path, 'r') as f:
        data = json.load(f)

    new_embed = discord.Embed(
        title=data["Title"],
        description=data["Description"],
        colour=discord.Colour.random()
    )
    new_embed.set_footer(text='Contact Nicholas_Lin#7193 with concerns.')
    new_embed.set_image(
        url=data["Image"])
    new_embed.set_thumbnail(
        url=data["Thumbnail"])
    new_embed.add_field(name="Time Remaining: ", value=message,
                        inline=True)
    new_embed.add_field(name=data['Field Name 2'], value=data['Field Value 2'],
                        inline=True)
    pfp = "https://cdn.discordapp.com/avatars/" + data["Author Icon"]
    new_embed.set_author(name=data["Author Name"],
                         icon_url=pfp)
    return new_embed


def set_embed(message, messageID, guildID):
    path = 'countdown-data.json'

    with open(path, 'r') as f:
        data = json.load(f)

    new_embed = discord.Embed(
        title=data[str(guildID)][str(messageID)]["Title"],
        description=data[str(guildID)][str(messageID)]["Description"],
        colour=discord.Colour.random()
    )
    new_embed.set_footer(text='Contact Nicholas_Lin#7193 with concerns.')
    new_embed.set_image(
        url=data[str(guildID)][str(messageID)]["Image"])
    new_embed.set_thumbnail(
        url=data[str(guildID)][str(messageID)]["Thumbnail"])
    new_embed.add_field(name="Time Remaining: ", value=message,
                        inline=False)
    new_embed.add_field(name=data[str(guildID)][str(messageID)]['Field Name 2'],
                        value=data[str(guildID)][str(messageID)]['Field Value 2'],
                        inline=False)
    pfp = "https://cdn.discordapp.com/avatars/" + data[str(guildID)][str(messageID)]["Author Icon"]
    new_embed.set_author(name=data[str(guildID)][str(messageID)]["Author Name"],
                         icon_url=pfp)
    return new_embed


def details_embed():
    path = 'temp-data.json'
    with open(path, 'r') as f:
        data = json.load(f)

    if data['Title'] == '':
        title_bool = '❌ Title'
    else:
        title_bool = '✅ Title: ' + data['Title']
    if data['Description'] == '':
        desc_bool = '❌ Description'
    else:
        desc_bool = '✅ Description: ' + data['Description']
    if data['Field Value'] == '':
        time_bool = '❌ *End time <YYYY-MM-DD HH:mm:ss>'
    else:
        time_bool = '✅ *End time: ' + data['Field Value']
    if data['Thumbnail'] == '':
        thumbnail_bool = '❌ Thumbnail'
    else:
        thumbnail_bool = '✅ Thumbnail: ' + data['Thumbnail']
    if data['Image'] == '':
        image_bool = '❌ Image'
    else:
        image_bool = '✅ Image: ' + data['Image']
    if data['Message'] == '':
        msg_bool = '❌ Countdown Message'
    else:
        msg_bool = '✅ Countdown Message: ' + data['Message']
    if data['Mention'] == '':
        mention_bool = '❌ Countdown Mention'
    else:
        mention_bool = '✅ Countdown Mention: ' + data['Mention']
    if data['Channel'] == 'countdown-announcements':
        channel_bool = '❌ Countdown Message Channel'
    else:
        channel_bool = '✅ Countdown Message Channel: #' + data['Channel']

    iterable = [title_bool, desc_bool, time_bool, thumbnail_bool, image_bool, msg_bool, mention_bool, channel_bool,
                "", "* = Mandatory Section"]
    separator = '\n'
    new_embed = discord.Embed(
        title="You've added the following:",
        description=separator.join(iterable),
        colour=discord.Colour.blue()
    )
    new_embed.set_footer(text='Contact Nicholas_Lin#7193 with concerns.')
    return new_embed


def help_embed():
    iterable = ["Countdown Buddy is a customizable countdown bot, read below to learn how to use it!",
                " ",
                "**Countdown Commands** ⏰",
                "**$new** - Creates a new countdown.",
                "**$countdown** - Starts the countdown.",
                "**$end <Countdown ID>** - Ends the specific countdown.",
                " ",
                "**Customizing Your Countdown** ⏰",
                "**set title <Insert Title>** - Set your title.",
                "**set description <Insert Description>** - Set your description.",
                "**set time <YYYY-MM-DD HH:mm:ss>** - Set your time (24-hour clock).",
                "**set thumbnail <Insert Thumbnail URL>** - Set your thumbnail.",
                "**set image <Insert Image URL>** - Set your image.",
                "**set message <Insert Message>** - Set the message for when countdown ends.",
                "**set mention <everyone/here/me>** - Set the mention for when countdown ends.",
                "**set channel <Channel name>** - Set the channel where the message is sent."
]

    separator = '\n'
    helpEmbed = discord.Embed(
        title="Countdown Buddy",
        description=separator.join(iterable),
        colour=discord.Colour.gold()
    )
    helpEmbed.set_thumbnail(url="https://media.discordapp.net/attachments/459383149068288032/851565274892861520/ctdico.png")
    helpEmbed.set_footer(text='Contact Nicholas_Lin#7193 with concerns.')
    return helpEmbed


