from urlextract import URLExtract
import pandas as pd
from collections import Counter
from wordcloud import WordCloud,STOPWORDS
import emoji


extract = URLExtract()

def userAnalytics(selected_user,df):
    if selected_user != "All users":
        df = df[df['Users'] == selected_user]

    # Number of messages sent
    nums_messages = df.shape[0]
    
    # Number of words
    words = []
    for message in df['Messages']:
        words.extend(message.split())
    
    # Counting the number of media shared
    media_omitted = df[df['Messages'] == '<Media omitted>']
    
    # Number of Links shared
    links = []
    for message in df['Messages']:
        links.extend(extract.find_urls(message))
        
    return nums_messages, len(words), media_omitted.shape[0], len(links)


def activeUserAnalytics(df):
    df = df[df['Users'] != 'Group Notification']
    count = df['Users'].value_counts().head()
    
    new_df = pd.DataFrame((df['Users'].value_counts()/df.shape[0])*100)
    return count, new_df




def createWordCloud(selected_user,df):
    if selected_user != "All users":
        df = df[df['Users'] == selected_user]
    
    wc = WordCloud(stopwords = STOPWORDS, width = 500,
               height = 500, random_state=42, min_font_size = 10, 
               background_color = 'white')
    
    df_img = wc.generate(df['Messages'].str.cat(sep = " "))
    return df_img


def getCommonWords(selected_user,df):
    
    file = open("stop_hinglish.txt", "r")
    stopwords = file.read()
    stopwords = stopwords.split("\n")
    if selected_user != "All users":
        df = df[df['Users'] == selected_user]
    
    temp = df[(df['Users'] != 'Group Notification') |
              (df['Users'] != '<Media omitted>')]

    words = []

    for message in temp['Messages']:
        for word in message.lower().split():
            if word not in stopwords:
                words.append(word)

    mostcommon = pd.DataFrame(Counter(words).most_common(20))
    return mostcommon


def getEmojiAnalysis(selected_user,df):
    if selected_user != "All users":
        df = df[df['Users'] == selected_user]
    
    emojis = []
    for message in df['Messages']:
        emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])
        
    emojidf = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emojidf


def getMonthlyTimeline(selected_user,df):
    if selected_user != "All users":
        df = df[df['Users'] == selected_user]
    temp = df.groupby(['Year','Month_num','Month']).count()['Messages'].reset_index()
        
    time = []
            
    for i in range(temp.shape[0]):
        time.append(str(temp['Month'][i]) + "-" + str(temp['Year'][i]))
            
    temp['Time'] = time
        
    return temp