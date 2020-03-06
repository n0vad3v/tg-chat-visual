from bs4 import BeautifulSoup
from datetime import datetime
from emoji import UNICODE_EMOJI
import os
import csv

def contain_emojis(chat):
    return chat in UNICODE_EMOJI

with open('chat_history.csv','w') as csv_file:
    field_names = ['from_name','msg_text','date','time','contains_emoji']
    writer = csv.writer(csv_file)
    writer.writerow(field_names)

    file_list = os.listdir(".")
    file_list.sort()

    for filename in file_list:
        if filename.endswith(".html"):
            with open(filename) as f:
                soup = BeautifulSoup(f,'html.parser')

                msg_list = soup.find_all(class_='message')
                emoji_msg = False
                for msg in msg_list[1:]:
                    try:
                        from_name = msg.find(class_='from_name').get_text().replace('\n','').strip(' ')
                    except:
                        continue
                    try:
                        msg_text = msg.find(class_='text').get_text().replace('\n','').strip(' ')
                        if contain_emojis(msg_text):
                            emoji_msg = True
                    except:
                        continue
                    
                    # 09.12.2018 17:18:19
                    raw_datetime = msg.find(class_='date').get('title')
                    tg_datetime_format = '%d.%m.%Y %H:%M:%S'
                    parsed_datetime = datetime.strptime(raw_datetime,tg_datetime_format)
                    # 2018-09-12
                    good_date = parsed_datetime.strftime("%Y-%m-%d")
                    # 17:18:19
                    good_time = parsed_datetime.strftime("%H:%M:%S")
                    
                    # Write to csv
                    writer.writerow([from_name,msg_text,good_date,good_time,emoji_msg])

