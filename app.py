import streamlit as st
import preprocess
import stats
import matplotlib.pyplot as plt
import numpy as np


st.sidebar.title("Watsapp Chat Analyzer")
uploaded_file = st.sidebar.file_uploader("Upload a file")

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = str(bytes_data,'UTF-8')
    
    df = preprocess.preprocess(data)
    # st.dataframe(df)
    
    users_list = list(df['Users'].unique())
    users_list.remove("Group Notification")
    
    users_list.sort()
    
    users_list.insert(0,"All users")
    
    selected_user = st.sidebar.selectbox("Showing Analysis with respect to", users_list)
    
    st.title("Watsapp Chat Analysis for " + selected_user)
    
    if st.sidebar.button("Show Analysis"):
        # USER ANALYTICS
        nums_messages, num_words, media_omitted, links = stats.userAnalytics(
            selected_user,df)
    
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.header("Number of Messages ")
            st.title(nums_messages)
        with col2:
            st.header("Number of Words ")
            st.title(num_words)
        with col3:
            st.header("Number of Media shared ")
            st.title(media_omitted)
        with col4:
            st.header("Number of Links shared ")
            st.title(links)
        
        # MOST ACTIVE USERS
        if selected_user == "All users":
            st.title("Most Active Users ")
            col1, col2 = st.columns(2)
            activeCount, new_df = stats.activeUserAnalytics(df)
            fig, ax = plt.subplots()
        
            with col1:
                ax.bar(activeCount.index,activeCount.values, color = 'black')
                plt.xticks(rotation = 'vertical')
                st.pyplot(fig)
            
            with col2:
                st.dataframe(new_df)
        
        # WORD CLOUD
        st.title("Word Cloud ")
        df_img = stats.createWordCloud(selected_user,df)
        fig,ax = plt.subplots()
        ax.imshow(df_img,interpolation="None")
        ax.axis("off")
        st.pyplot(fig)
        
        # Most Common words used
        st.title("Most Common Words Used ")
        most_common_df = stats.getCommonWords(selected_user,df)
        fig, ax = plt.subplots()
        ax.barh(most_common_df[0], most_common_df[1],color='black')
        plt.xticks(rotation = "vertical")
        st.pyplot(fig)
        
        
        # Emoji Analysis
        st.title("Emoji Analysis")
        emoji_df = stats.getEmojiAnalysis(selected_user,df)
        emoji_df.columns = ['Emoji', 'Count']
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.dataframe(emoji_df)
        
        with col2:
            emojicount = list(emoji_df['Count'])
            sumOfAllEmojisUsed = 0
            for i in emojicount:
                sumOfAllEmojisUsed += int(i) 
            perlist = [(int(i)/sumOfAllEmojisUsed)*100 for i in emojicount]
            emoji_df['Percentage Use'] = np.array(perlist)
            st.dataframe(emoji_df)
            
            
        # Monthly Timeline
        st.title("Monthly Timeline ")
        time = stats.getMonthlyTimeline(selected_user,df)
        fig, ax = plt.subplots()
        ax.plot(time['Time'],time['Messages'],color = 'black')
        plt.xticks(rotation = 'vertical')
        plt.tight_layout()
        st.pyplot(fig)
        