import json
import discord
from util import countdownEmbeds
from datetime import datetime

# compare the time the user entered and the current time to see if countdown is possible
def check_time_validity(endtime):
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
    if date_now_timestamp >= last_day_timestamp:
        return True
    else:
        return False

# method to update countdown
async def update_countdown(guild, messageID):
    try:
        # see if a countdown channel exists
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
            channel_name = data[str(guild.id)][str(messageID)]['Channel']
            if discord.utils.get(guild.channels, name=channel_name) is None:
                cd_announcements_channel = await guild.create_text_channel(channel_name)
                await cd_announcements_channel.edit(position=0, sync_permissions=True)
            else:
                cd_announcements_channel = discord.utils.get(guild.channels, name=channel_name)

            send_countdown_message = data[str(guild.id)][str(messageID)]['Message']
            send_countdown_ping = data[str(guild.id)][str(messageID)]['Mention']

            end_embed = countdownEmbeds.set_embed("Timer has ended!", messageID, guild.id)
            cd_message = await cd_channel.fetch_message(messageID)
            await cd_message.edit(embed=end_embed)

            del data[str(guild.id)][str(messageID)]

            with open(path, 'w') as f:
                json.dump(data, f, indent=4)

            if send_countdown_ping == 'here':
                await cd_announcements_channel.send("@here")
            elif send_countdown_ping == "everyone":
                await cd_announcements_channel.send("@everyone")
            elif send_countdown_ping.startswith("<@!"):
                try:
                    await cd_announcements_channel.send(send_countdown_ping)
                except Exception as e:
                    print(e)
            await cd_announcements_channel.send(send_countdown_message)

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
                                        'Author Icon': tempDict['Author Icon'], 'Channel': tempDict['Channel']}}
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
                try:
                    delete_message = await cd_channel.fetch_message(messageID)
                    await delete_message.delete()
                except Exception as e:
                    print("Someone deleted the countdown!")

                new_message = countdownEmbeds.set_embed(new_time, messageID, guild.id)
                message = await cd_channel.send(embed=new_message)
                data[str(guild.id)][str(message.id)] = data[str(guild.id)][str(messageID)]
                data[str(guild.id)][str(message.id)]['Field Value 2'] = str(message.id)
                del data[str(guild.id)][str(messageID)]
                with open(path, 'w') as f:
                    json.dump(data, f, indent=4)
    except Exception as e:
        print(f"leaderboard error in server {guild.name}")
        print(e)
