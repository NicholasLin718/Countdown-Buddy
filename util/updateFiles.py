import json


def write_file(guildID):
    temp_path = '../temp-data.json'
    with open(temp_path, 'r') as f:
        temp_file_data = json.load(f)

    path = '../countdown-data.json'
    with open(path, 'r') as f:
        data = json.load(f)
        temp = data[str(guildID)]
        # append new server data to dict
        append = {"temp": {'Title': temp_file_data['Title'], 'Description': temp_file_data['Description'],
                           'Field Name': 'Time Remaining: ', 'Field Value': temp_file_data['Field Value'],
                           'Field Name 2': temp_file_data['Field Name 2'],
                           'Field Value 2': temp_file_data['Field Value 2'],
                           'Image': temp_file_data['Image'], 'Thumbnail': temp_file_data['Thumbnail'],
                           'Message': temp_file_data['Message'], 'Mention': temp_file_data['Mention'],
                           'Author Name': temp_file_data['Author Name'], 'Author Icon': temp_file_data['Author Icon'],
                           'Channel': temp_file_data['Channel']}}
        temp.update(append)
    # write updated dict to file
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)

    append = {'Title': '', 'Description': '', 'Field Name': 'Time Remaining: ',
              'Field Value': '', 'Field Name 2': 'Message ID: ', 'Field Value 2': '0',
              'Image': '', 'Thumbnail': '',
              'Message': '', 'Mention': '', 'Author Name': '',
              'Author Icon': '', 'Channel': 'countdown-announcements'}
    temp_file_data.update(append)
    with open(temp_path, 'w') as f:
        json.dump(temp_file_data, f, indent=4)


def write_temp(countdown_title, countdown_description, countdown_time, countdown_image, countdown_thumbnail, countdown_msg, countdown_mention, countdown_author_name, countdown_author_icon, countdown_announcement_channel):
    path = '../temp-data.json'
    with open(path, 'r') as f:
        data = json.load(f)
    # append new server data to dict
    append = {'Title': countdown_title, 'Description': countdown_description, 'Field Name': 'Time Remaining: ',
              'Field Value': countdown_time, 'Field Name 2': 'Message ID: ', 'Field Value 2': '0',
              'Image': countdown_image, 'Thumbnail': countdown_thumbnail,
              'Message': countdown_msg, 'Mention': countdown_mention, 'Author Name': countdown_author_name,
              'Author Icon': countdown_author_icon, 'Channel': countdown_announcement_channel}
    data.update(append)
    # write updated dict to file
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)