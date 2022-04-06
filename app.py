# This file contains the main application file for our web applet.

import streamlit as st 
import wordcloud
from funcs import words_from_tweet
import matplotlib.pyplot as plt

if __name__ == '__main__':
    st.title("Twitter WordCloud Generator")
    st.write("Hello! This web app allows you to generate a word cloud from the tweets of any Twitter user of your choice. Type the exact Twitter username (without the @) and configure the settings on the side bar before clicking the 'Generate Wordcloud' button. Enjoy!")

    # Configuring the sidebar widgets
    with st.sidebar:
        with st.form(key = 'form'):
            username = st.text_input("Type the username below.")
            criteria = st.selectbox("Choose the criteria for fetching Tweets.", ["most recent","most popular"])
            limit = st.slider("Choose how many tweets would you like to fetch.", min_value=200, max_value=3000, value=1600, step=100)
            background = st.selectbox("Choose the background color for your wordcloud.", ["black", "white"])
            style = st.selectbox("Choose a wordcloud style.", ['viridis', 'plasma', 'inferno', 'magma', 'cividis','Pastel1', 'Pastel2', 'Paired', 'Accent', 'flag', 'prism', 'ocean', 'gist_earth', 'terrain', 'gist_stern', 'rainbow', 'jet', 'turbo', 'gray', 'bone', 'pink', 'spring', 'summer', 'autumn', 'winter', 'cool', 'hot', 'copper'])
            submit = st.form_submit_button('Generate WordCloud') 

    # Configuring applet response to form submission
    if submit:
        with st.spinner("Please wait while your wordcloud is being generated..."):
            try:
                cloud = wordcloud.WordCloud(background_color=background, colormap=style).generate(words_from_tweet(username,criteria,limit))
                fig = plt.figure()
                plt.imshow(cloud)
                plt.axis("off")
                st.header(f"Wordcloud from the {limit} {criteria} tweets of @{username}")
                st.pyplot(fig)
                st.write("To create more wordclouds, configure the settings on the sidebar and click the 'Generate Wordcloud' button.")
            except:
                st.header(f"There has been an error in fetching the tweets of @{username}. Please make sure that the username you entered is valid.")

