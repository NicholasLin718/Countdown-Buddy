import json
import discord
from util import countdownEmbeds
from datetime import datetime
from pymongo import MongoClient

f = open("password.txt", "r")
PASSWORD = f.read()

cluster = MongoClient("mongodb+srv://nicholas_lin:" + PASSWORD + "@cluster0.dsz7w.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

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
    db = cluster["countdown-buddy"]
    collection = db["countdown-data"]
    try:
        # see if a countdown channel exists
        if discord.utils.get(guild.channels, name='countdown') is None:
            cd_channel = await guild.create_text_channel('countdown')
            await cd_channel.edit(position=0, sync_permissions=True)
        else:
            cd_channel = discord.utils.get(guild.channels, name='countdown')

        # path = 'countdown-data.json'
        # with open(path, 'r') as f:
        #     data = json.load(f)
        # get the end time of that countdown
        data = collection.find_one({"_id": messageID})
        time = data[str("Field Value")]
        new_time = await countdownEmbeds.new_msg(cd_channel, time)
        # if the endtime has already passed and new_time stored a return value of "Timer has ended."
        if new_time == "Timer has ended.":
            channel_name = data['Channel']
            if discord.utils.get(guild.channels, name=channel_name) is None:
                cd_announcements_channel = await guild.create_text_channel(channel_name)
                await cd_announcements_channel.edit(position=0, sync_permissions=True)
            else:
                cd_announcements_channel = discord.utils.get(guild.channels, name=channel_name)
            send_countdown_message = data['Message']
            send_countdown_ping = data['Mention']
            # edit the message to say the timer has ended
            end_embed = countdownEmbeds.set_embed("Timer has ended!", messageID, guild.id)
            cd_message = await cd_channel.fetch_message(messageID)
            await cd_message.edit(embed=end_embed)
            collection.delete_one({"id_": messageID})
            # del data[str(guild.id)][str(messageID)]

            # with open(path, 'w') as f:
            #     json.dump(data, f, indent=4)
            # ping the mention the user chose, or no ping at all
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
        # replace the new countdown using messageID as the new key
        elif messageID == guild.id:            
            # path = 'countdown-data.json'
            # with open(path, 'r') as f:
            #     countdown_data = json.load(f)
            #     print(countdown_data)
            new_message = countdownEmbeds.set_temp_embed(new_time, guild.id)
            message = await cd_channel.send(embed=new_message)
            tempDict = collection.find_one({"_id": guild.id})
            post = {"_id": message.id, 'Title': tempDict['Title'], 'Description': tempDict['Description'], 'Field Name': "Time Remaining: ",
                                        'Field Value': tempDict['Field Value'], 'Field Name 2': "Message ID",
                                        'Field Value 2': message.id, 'Image': tempDict['Image'],
                                        'Thumbnail': tempDict['Thumbnail'], 'Message': tempDict['Message'],
                                        'Mention': tempDict['Mention'], 'Author Name': tempDict['Author Name'],
                                        'Author Icon': tempDict['Author Icon'], 'Channel': tempDict['Channel'],
                                        'GuildID': guild.id}
            collection.insert_one(post)
            collection.delete_one({"_id": guild.id})
        # any other situation - edits the message with a new time
        else:
            try:
                cd_message = await cd_channel.fetch_message(messageID)
                new_message = countdownEmbeds.set_embed(new_time, messageID, guild.id)
                await cd_message.edit(embed=new_message)
            except Exception as e:  # if bot can't edit a message, delete message and send a new one
                print(f"countdown edit error: {e}")
                try:
                    delete_message = await cd_channel.fetch_message(messageID)
                    await delete_message.delete()
                except Exception as e:
                    print("Someone deleted the countdown!")
                    
                new_message = countdownEmbeds.set_embed(new_time, messageID, guild.id)
                message = await cd_channel.send(embed=new_message)
                
                
                # collection.update_one({"_id": messageID}, {"$set":{"_id": message.id}})
                
                newPost = collection.find_one({"_id": messageID})
                newPost["_id"] = message.id
                newPost["Field Value 2"] = message.id
                collection.delete_one({"_id": messageID})
                collection.insert_one(newPost)
                
                # data[str(guild.id)][str(message.id)] = data[str(guild.id)][str(messageID)]
                # data[str(guild.id)][str(message.id)]['Field Value 2'] = str(message.id)
                # del data[str(guild.id)][str(messageID)]
                # with open(path, 'w') as f:
                #     json.dump(data, f, indent=4)

    except Exception as e:
        print(f"countdown error in server {guild.name}")
        print(e)
