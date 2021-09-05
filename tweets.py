import os
import twitter
import tweepy as tw
import pandas as pd

class tweet_function:
    def tweet(name):
        # Keys and token
        CONSUMER_KEY    = "Your key"
        CONSUMER_SECRET = "Your key"
        ACCESS_KEY      = "Your key"
        ACCESS_SECRET   = "Your key"
        # Authentication
        auth = tw.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
        api = tw.API(auth, wait_on_rate_limit=True)
        # CallingAPI
        api = tw.API(auth)
        # Pulling data
        screen_name = name
        user = api.get_user(screen_name)
        tweets = tw.Cursor(api.user_timeline,id=screen_name).items(10)
        tweets_list = [[tweet.created_at, tweet.id, tweet.text] for tweet in tweets]
        return tweets_list
