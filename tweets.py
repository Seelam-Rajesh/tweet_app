import os
import twitter
import tweepy as tw
import pandas as pd

class tweet_function:
    def tweet(name):
        # Update Keys and token
        CONSUMER_KEY    = "Your Secret Key" 
        CONSUMER_SECRET = "Your Secret Key"
        ACCESS_KEY      = "Your Secret Key"
        ACCESS_SECRET   = "Your Secret Key"
        # Authentication
        auth = tw.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
        api = tw.API(auth, wait_on_rate_limit=True)
        # CallingAPI
        api = tw.API(auth)
        # Pulling data
        screen_name = name
        user = api.get_user(screen_name)
        tweets = tw.Cursor(api.user_timeline,id=screen_name).items(20)
        return tweets
