import json
import discord
import countdownEmbeds
from datetime import timedelta, datetime


# def check_expiry(client):
#     path = 'countdown-data.json'
#     with open(path, 'r') as f:
#         data = json.load(f)
#     new_data = {}
#     for x in client.guilds:
#         for y in data[str(x.id)]:
#             is_expired = check_countdown_expire(data[str(x.id)][str(y)]['Field Value'])
#             if not is_expired:
#                 append = {str(x.id): data[str(x.id)][str(y)]}
#                 new_data.update(append)
#     with open(path, 'w') as f:
#         json.dump(new_data, f, indent=4)
#
#     print(new_data)



def check_countdown_expire(endtime):
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
        return True
    else:
        return False


async def update_countdown(guild, messageID):
    # try:
        if discord.utils.get(guild.channels, name='countdown') is None:
            cd_channel = await guild.create_text_channel('countdown')
            await cd_channel.edit(position=0, sync_permissions=True)
        else:
            cd_channel = discord.utils.get(guild.channels, name='countdown')

        path = 'countdown-data.json'
        with open(path, 'r') as f:
            data = json.load(f)

        time = data[str(guild.id)][str(messageID)][str("Field Value")]
        new_time = await countdownEmbeds.new_msg(cd_channel, time)
        if new_time == "Timer has ended.":
            path = 'countdown-data.json'
            with open(path, 'r') as f:
                data = json.load(f)

            send_countdown_message = data[str(guild.id)][str(messageID)]['Message']
            send_countdown_ping = data[str(guild.id)][str(messageID)]['Mention']
            del data[str(guild.id)][str(messageID)]

            with open(path, 'w') as f:
                json.dump(data, f, indent=4)

            end_embed = countdownEmbeds.set_embed("Timer has ended!", messageID, guild.id)
            cd_message = await cd_channel.fetch_message(messageID)
            await cd_message.edit(embed=end_embed)
            if send_countdown_ping == 'here':
                await cd_channel.send("@here")
                await cd_channel.send(send_countdown_message)
            elif send_countdown_ping == "everyone":
                await cd_channel.send("@everyone")
                await cd_channel.send(send_countdown_message)
            elif send_countdown_ping.startswith("<@!"):
                try:
                    await cd_channel.send(send_countdown_ping)
                except Exception as e:
                    print(e)
                await cd_channel.send(send_countdown_message)

        elif messageID == "temp":
            new_message = countdownEmbeds.set_temp_embed(new_time)
            message = await cd_channel.send(embed=new_message)
            tempDict = data[str(guild.id)]["temp"]
            append = {str(message.id): {'Title': tempDict['Title'], 'Description': tempDict['Description'],
                                        'Field Name': "Time Remaining: ",
                                        'Field Value': tempDict['Field Value'], 'Field Name 2': "Message ID",
                                        'Field Value 2': str(message.id), 'Image': tempDict['Image'],
                                        'Thumbnail': tempDict['Thumbnail'], 'Message': tempDict['Message'],
                                        'Mention': tempDict['Mention'], 'Author Name': tempDict['Title'],
                                        'Author Icon': tempDict['Author Icon']}}
            data[str(guild.id)].update(append)
            del data[str(guild.id)]["temp"]
            with open(path, 'w') as f:
                json.dump(data, f, indent=4)
        else:
            try:
                cd_message = await cd_channel.fetch_message(messageID)
                new_message = countdownEmbeds.set_embed(new_time, messageID, guild.id)
                await cd_message.edit(embed=new_message)
            except Exception as e:  # if bot can't edit a message, reset channel and display a new leaderboard
                print(f"leaderboard edit error: {e}")
                delete_message = await cd_channel.fetch_message(messageID)
                await delete_message.delete()
                new_message = countdownEmbeds.set_embed(new_time, messageID, guild.id)
                message = await cd_channel.send(embed=new_message)
                data[str(message.id)] = data[str(messageID)]
                del data[str(messageID)]
                with open(path, 'w') as f:
                    json.dump(data, f, indent=4)
    # except Exception as e:
    #     print(f"leaderboard error in server {guild.name}")
    #     print(e)
