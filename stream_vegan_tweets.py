# -*- coding: utf-8 -*-
"""
Created on Sun Feb 25 15:04:25 2018

@author: Yunshi_Zhao
"""

import pandas as pd
import requests
import cnfg
import json
import tweepy

from pymongo import MongoClient
from requests_oauthlib import OAuth1


def stream_tweet(query, collection):   
    config = cnfg.load("/home/ubuntu/Documents/.twitter_config")
    
    auth = tweepy.OAuthHandler(config["consumer_key"],
                               config["consumer_secret"])
    auth.set_access_token(config["access_token"],
                          config["access_token_secret"])
    api=tweepy.API(auth)
    
    class StreamListener(tweepy.StreamListener):
    
        def on_status(self, status):
            
            # skip retweets
           # if status.retweeted: 
               # return
        
            # store tweet and creation date
            data = {}
            data['id'] = status.id
            data['datetime'] = status.created_at
            try:
                data['text'] = status.extended_tweet['full_text']
            except:
                data['text'] = status.text
            data['entities'] = status.entities
            data['reply_to_tweet'] = status.in_reply_to_status_id
            data['user'] = status.user.id
            data['retweet_count'] = status.retweet_count
            data['favorite_count'] = status.favorite_count
            #data['possibly_sensitive'] = status.possibly_sensitive
            data['lang'] = status.lang
    
            # insert into db
            try:
                collection.insert_one(data)
            except:
                pass
    
    stream_listener = StreamListener()
    stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
    stream.filter(track=[query])
    
if __name__ == "__main__":
    client = MongoClient(port=27017)
    db = client.tweet_on_vegan
    vegan_tweets = db.streaming_tweets
    stream_tweet("vegan", vegan_tweets)
