import re
import pandas as pd


def getTimeAndDate(string):
    string = string.split(",")
    date,time = string[0], string[1]
    time = time.split(' ')
    final_time = time[1].strip()
    if time[2] == 'pm':
        hour,minutes = time[1].split(':')
        hour = int(hour) + 12
        if hour == 24:
            hour = '00'
        final_time = str(hour) + ":"+ str(minutes)
    
    return date + " " + final_time  

def preprocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s..\s-\s'
    messages = re.split(pattern, data)
    dates = re.findall(pattern, data)
    p = messages.count('pm')
    a = messages.count('am')
    print(dates)
    print(len(dates))
    
    for i in range(p):
        messages.remove('pm')
    for i in range(a):
        messages.remove('am')
    print(len(messages))
    
    

    df = pd.DataFrame({'user_messages': messages[1:],
                       'message_date': dates})

    df['message_date'] = df['message_date'].apply(
        lambda text: getTimeAndDate(text))
    df.rename(columns={'message_date': 'Date'}, inplace=True)
    
    users = []
    messages = []
    
    for message in df['user_messages']:
        entry = re.split('([\w\W]+?):\s',message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append("Group Notification")
            messages.append(entry[0])
    
    df['Users'] = users
    df['Messages'] = messages
    
    df['Messages'] = df['Messages'].apply(lambda text: text.split('\n')[0])
    
    df.drop(['user_messages'], inplace=True, axis=1)
    df = df[['Messages','Date','Users']]
    
    df['Only date'] = pd.to_datetime(df['Date']).dt.date

    df['Year'] = pd.to_datetime(df['Date']).dt.year

    df['Month_num'] = pd.to_datetime(df['Date']).dt.month

    df['Month'] = pd.to_datetime(df['Date']).dt.month_name()

    df['Day'] = pd.to_datetime(df['Date']).dt.day

    df['Day_name'] = pd.to_datetime(df['Date']).dt.day_name()

    df['Hour'] = pd.to_datetime(df['Date']).dt.hour

    df['Minute'] = pd.to_datetime(df['Date']).dt.minute
    
    return df