import json
from pymongo import MongoClient

def write_file(guildID):
    
    f = open("password.txt", "r")
    PASSWORD = f.read()

    cluster = MongoClient("mongodb+srv://nicholas_lin:" + PASSWORD + "@cluster0.dsz7w.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

    db = cluster["countdown-buddy"]
    collection = db["countdown-data"]
    
    countdown_path = 'countdown-data.json'
    with open(countdown_path, 'r') as f:
        countdown_file = json.load(f)
        countdown_file_data = countdown_file[str(guildID)]
            
        post = {"_id": guildID, 'Title': countdown_file_data['Title'], 'Description': countdown_file_data['Description'],
                                    'Field Name': "Time Remaining: ",
                                    'Field Value': countdown_file_data['Field Value'], 'Field Name 2': "Message ID",
                                    'Field Value 2': guildID, 'Image': countdown_file_data['Image'],
                                    'Thumbnail': countdown_file_data['Thumbnail'], 'Message': countdown_file_data['Message'],
                                    'Mention': countdown_file_data['Mention'], 'Author Name': countdown_file_data['Author Name'],
                                    'Author Icon': countdown_file_data['Author Icon'], 'Channel': countdown_file_data['Channel'],
                                    'GuildID': guildID}
        collection.insert_one(post)
        # transport all the values from temp-data to countdown-data under the key "temp"
        # append = {"temp": {'Title': countdown_file_data['Title'], 'Description': countdown_file_data['Description'],
        #                    'Field Name': 'Time Remaining: ', 'Field Value': countdown_file_data['Field Value'],
        #                    'Field Name 2': countdown_file_data['Field Name 2'],
        #                    'Field Value 2': countdown_file_data['Field Value 2'],
        #                    'Image': countdown_file_data['Image'], 'Thumbnail': countdown_file_data['Thumbnail'],
        #                    'Message': countdown_file_data['Message'], 'Mention': countdown_file_data['Mention'],
        #                    'Author Name': countdown_file_data['Author Name'], 'Author Icon': countdown_file_data['Author Icon'],
        #                    'Channel': countdown_file_data['Channel']}}
        # temp.update(append)
    # write updated dict to file
    with open(countdown_path, 'w') as f:
        json.dump(countdown_file, f, indent=4)

    # append = {}
    # countdown_file_data.update(append)
    # with open(countdown_path, 'w') as f:
    #     json.dump(countdown_file, f, indent=4)

    


def write_temp(countdown_title, countdown_description, countdown_time, countdown_image, countdown_thumbnail, countdown_msg, countdown_mention, countdown_author_name, countdown_author_icon, countdown_announcement_channel, guildID):
    path = 'countdown-data.json'
    
    with open(path, 'r') as f:
        d = json.load(f)
    # append values to the temp-data file, where all the values the user is entering before the countdown starts is stored
    data = d[str(guildID)]
    append = {'Title': countdown_title, 'Description': countdown_description, 'Field Name': 'Time Remaining: ',
              'Field Value': countdown_time, 'Field Name 2': 'Message ID: ', 'Field Value 2': guildID,
              'Image': countdown_image, 'Thumbnail': countdown_thumbnail,
              'Message': countdown_msg, 'Mention': countdown_mention, 'Author Name': countdown_author_name,
              'Author Icon': countdown_author_icon, 'Channel': countdown_announcement_channel}
    data.update(append)
    # write updated dict to file
    with open(path, 'w') as f:
        json.dump(d, f, indent=4)
