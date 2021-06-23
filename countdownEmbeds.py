import json
from datetime import timedelta, datetime

import discord


async def update_msg(new_message, msg):
    await msg.edit(content=new_message)


async def send_msg(guild, countdown):
    new_message = await guild.send(content=countdown)
    return new_message.id


def new_msg(endtime):
    y = int(endtime[0:4])
    m = int(endtime[5:7])
    d = int(endtime[8:10])
    h = int(endtime[11:13])
    min = int(endtime[14:16])
    s = int(endtime[17:19])

    date_now = datetime.today()
    date_now_timestamp = int(date_now.timestamp())
    last_day_date = datetime(year=y, month=m, day=d, hour=h, minute=min, second=s)
    last_day_timestamp = int(last_day_date.timestamp())
    remaining_time_seconds = last_day_timestamp - date_now_timestamp

    remaining_time = timedelta(seconds=remaining_time_seconds)
    remaining_days = remaining_time.days
    remaining_seconds = remaining_time.seconds

    remaining_minutes, remaining_seconds = divmod(remaining_seconds, 60)
    remaining_hours, remaining_minutes = divmod(remaining_minutes, 60)

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


def set_embed(message):
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
    new_embed.add_field(name="dababy", value=message,
                        inline=True)
    return new_embed

def details_embed():
    if countdown_title == '':
        title_bool = 'Title ❌'
    else:
        title_bool = 'Title ✅'
    if countdown_description == '':
        desc_bool = 'Description ❌'
    else:
        desc_bool = 'Description ✅'
    if countdown_time == '':
        time_bool = 'End time* ❌ <YYYY-MM-DD HH:mm:ss>'
    else:
        time_bool = 'End time* ✅'
    if countdown_thumbnail == '':
        thumbnail_bool = 'Thumbnail ❌'
    else:
        thumbnail_bool = 'Thumbnail ✅'
    if countdown_image == '':
        image_bool = 'Image ❌'
    else:
        image_bool = 'Image ✅'
    if countdown_msg == '':
        msg_bool = 'Countdown Message ❌'
    else:
        msg_bool = 'Countdown Message ✅'
    if countdown_mention == '':
        mention_bool = 'Countdown Mention ❌'
    else:
        mention_bool = 'Countdown Mention ✅'

    iterable = [title_bool, desc_bool, time_bool, thumbnail_bool, image_bool, msg_bool, mention_bool, "", "* = Mandatory Section"]
    separator = '\n'
    new_embed = discord.Embed(
        title="You've added the following:",
        description=separator.join(iterable),
        colour=discord.Colour.blue()
    )
    new_embed.set_footer(text='Contact Nicholas_Lin#7193 with concerns.')
    return new_embed

