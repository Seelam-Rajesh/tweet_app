import os
import twitter
import tweepy as tw
import pandas as pd

class tweet_function:
    def tweet(name):
        # Keys and token
        CONSUMER_KEY    = "18wZRgoLYoK7RCBSwzOxcjxsV"
        CONSUMER_SECRET = "0WgsV1Q7zaXjSOx25jJnc7pSExuONbncqd4WIXLTPJhMfjSvrT"
        ACCESS_KEY      = "2166758150-PxGU2TJfK8IxNPBJXy0oAI2WYwVli05LJW2lVs4"
        ACCESS_SECRET   = "mz41HwOy7J5i7caamXJKBzuc5OSolqPHePExNQVz7GBn8"
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