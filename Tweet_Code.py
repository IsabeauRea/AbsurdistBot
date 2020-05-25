# import packages
import tweepy
import tkinter
from textblob import TextBlob
import datetime
import sys
from time import sleep
import requests
import nltk
import re
import emoji
import random
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

# Retrieve a trending word from Google Trends using Selenium and headless Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome("/Users/Gingersnap/.wdm/drivers/chromedriver/81.0.4044.138/mac64/chromedriver", options=chrome_options)
google = "https://trends.google.com/trends/?geo=US"
driver.get(google)

# Retrieve the trending word from Google Trends
list_class = driver.find_elements_by_class_name("list-item-container")


length = len(list_class)
length = length - 1 
term_number = random.randint(0,length)

phrase = list_class[term_number].text
split_phrase = phrase.split(" ")
search_term = split_phrase[0]
print(search_term)


# All the API information
api_key = "gLObPtBSxKGZu2NfI4s0vxP68"
api_secret_key = "cfXBvP0JxAPWi0HU1vtkGQXMmXPpELxgCqnA5JcD7V3004yXzs"
access_token = '1244676478312349696-03mNJkgTNhWVRHtVPkcFdIrPIu4q5z'
access_token_secret = '7nHDttv1nxfJvdUkGwq3L2CQKRBzqs5JCNew3l5pfGrxM'

# Access Twitter API
auth = tweepy.OAuthHandler(api_key, api_secret_key)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Search for Tweets that contain the term retrieved from Google Trends
results = api.search(search_term, count = 200)

# An empty list for storing any tweet that has a positive connotation
positive_tweets = []

for result in results:
    analysis = TextBlob(result.text)
    sentiment = analysis.sentiment[0]

    if sentiment >= 0.20:
        if sentiment not in positive_tweets:
            positive_tweets.append(str(analysis))


positive_words = []

for result in positive_tweets:
    try:
        try:
            text = nltk.word_tokenize(result)
            word_type_tag = nltk.pos_tag(text)
            word_type_list = [word for word in word_type_tag]
            for word in word_type_list:
                positive_words.append(word)
        except:
            print("this word does not have a type")
    except:
        print("unfit sentence")

noun = 0 
verb = 0
adverb = 0

for word in positive_words:
    given_word = word[0]
    word_type = word[1]

    if "@" not in given_word:
        if "." not in given_word:
            if any(char.isdigit() for char in given_word) == False:
               
                analysis = TextBlob(given_word)
                sentiment = analysis.sentiment[0]

                if sentiment >= 0.01:
                    
                    if word_type == "NN":
                      noun = word[0]
                    
                    if word_type == "VB":
                        verb = word[0]
                    
                    if word_type == "RB":
                        adverb = word[0]


emoji_list = [emoji.emojize(':sparkling_heart:'), emoji.emojize(':sparkles:'), emoji.emojize(':bug:'),emoji.emojize(':confetti_ball:')]

index = random.randint(0,3)
emoji = emoji_list[index]

verb = str(verb) + "s"
string_format = "%s %s %s! %s" %(noun, verb, adverb, emoji)
print(string_format)

try:
    api.update_status(string_format)
    sleep(5)

except:
    print('already tweeted this particular tweet')
