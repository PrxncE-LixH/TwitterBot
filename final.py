import tweepy
import urllib3
import time
import os
from dotenv import load_dotenv, dotenv_values

# @PrxncE_LixH


# loading variables from .env file
load_dotenv('.env')

auth = tweepy.OAuthHandler(os.getenv("API_key"), os.getenv("API_key_Secret"))
auth.set_access_token(os.getenv("Access_Token"), os.getenv("Access_Token_Secret"))
api = tweepy.API(auth)


# this class is referenced from an open source project on github.com
# /Dhravya/beautify-this-bot/blob/9f57756fd064f42048237e4f55e2bb1ae31e5e62/src/main.py
# it esentially generates the tweet in a screenshot form and returns the path.
class generateLink:
    def get_poem(id, savepath="tweet.png"):
        poem_link = "https://beautify.dhravya.dev/tweet/" + str(id)
        http = urllib3.PoolManager()
        r = http.request('GET', poem_link)
        with open(savepath, 'wb') as f:
            f.write(r.data)
        return savepath


getLink = generateLink()  # generate link object


sinceID = 'lastID.txt'  # initial tweet ID


def readLastSeen(sinceID):
    readFile = open(sinceID, 'r')
    recentID = int(readFile.read().strip())
    readFile.close()
    return recentID


def saveLastSeen(sinceID, ID):
    writeFile = open(sinceID, 'w')
    writeFile.write(str(ID))
    writeFile.close()
    return


def replyWithMedia():

    # grab your recent mentions on the timeline greater than the passed tweet ID. Refer to tweepy Documentation for more information
    tweets = api.mentions_timeline(since_id=readLastSeen(sinceID))
    for tweet in reversed(tweets):
        # condition required to take a screenshot...the word "screenshot.."
        if "screenshot" in tweet.text.lower() or "screenshot this" in tweet.text.lower():
            print(str(tweet.id) + ' ---------- ' + tweet.text)

            # using the reply id , we are finding the original tweet to capture.
            getReply = api.get_status(id=tweet.id)
            findOriginalId = getReply.in_reply_to_status_id
            findOriginalTweet = api.get_status(findOriginalId)

            generateLink.get_poem(findOriginalTweet.id)
            api.update_status_with_media(
                f"@{tweet.user.screen_name}  Here's your request", filename="tweet.png", in_reply_to_status_id=tweet.id)  # make a tweet tagging the user with the media.

            # updating the sinceID to avoid replying to the same tweets
            saveLastSeen(sinceID, tweet.id)


while True:
    replyWithMedia()
    time.sleep(10)
