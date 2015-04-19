#  Calibretto 1.1
#  Calibretto allows you to choose keywords to track on
#  Twitter and store associated tweets in your database.

import sys
import twitter
from peewee import *


#  Twitter authentication
#  Grab your creds at https://apps.twitter.com
CONSUMER_KEY = "{Consumer Key (API Key)}"
CONSUMER_SECRET = "{Consumer Secret (API Secret)}"
OAUTH_TOKEN = "{Access Token}"
OAUTH_TOKEN_SECRET = "{Access Token Secret}"

auth = twitter.oauth.OAuth(OAUTH_TOKEN,
                           OAUTH_TOKEN_SECRET,
                           CONSUMER_KEY,
                           CONSUMER_SECRET)

twitter_api = twitter.Twitter(domain="api.twitter.com",
                              api_version="1.1",
                              auth=auth)


#  Connect to your PostgreSQL database
db = PostgresqlDatabase("{database}",
                        host="{host}",
                        port="{port}",
                        user="{username}",
                        password="{password}")


#  Choose keywords
harvest_list = ["{keyword1}","{keyword2}"]


#  Set up data classes
class BaseModel(Model):
    class Meta:
        database = db


class Temptweets(BaseModel):
    tweet_id = PrimaryKeyField()
    tweet_datetime = DateTimeField()
    tweet_keyword = CharField(max_length=50)
    tweet  = CharField(max_length=200)
    tweeter = CharField(max_length=50)
    lang = CharField(max_length=50)
    latitude = DoubleField()
    longitude = DoubleField()


class Tweets(BaseModel):
    tweet_id = PrimaryKeyField()
    tweet_datetime = DateTimeField()
    tweet_keyword = CharField(max_length=50)
    tweet  = CharField(max_length=200)
    tweeter = CharField(max_length=50)
    lang = CharField(max_length=50)
    latitude = DoubleField()
    longitude = DoubleField()


class Tweetlog(BaseModel):
    runid = PrimaryKeyField()
    batchid = IntegerField()
    rundate = DateTimeField()
    keyword = CharField(max_length=50)
    harvestedthisrun = IntegerField()
    totalharvested = IntegerField()


#  Set up app functions
def initialize():
    db.connect()


def get_tweets():
    for tweet_keyword in harvest_list:
        search_results = twitter_api.search.tweets(q=tweet_keyword,count=100)
        for status in search_results["statuses"]:
            if status["geo"]:
                tweet_id = status["id_str"]
                tweet_datetime = status["created_at"]
                tweet = status["text"]
                tweeter = "@" + status["user"]["screen_name"]
                lang = status["metadata"]["iso_language_code"]
                latitude = status["geo"]["coordinates"][0]
                longitude = status["geo"]["coordinates"][1]

                print("\n##\n"
                      "tweet_id: {}\n"
                      "tweet_datetime: {}\n"
                      "tweet_keyword: {}\n"
                      "tweet: {}\n"
                      "tweeter: {}\n"
                      "lang: {}\n"
                      "latitude: {}\n"
                      "longitude: {}\n"
                      "##".format(tweet_id,
                                  tweet_datetime,
                                  tweet_keyword,
                                  tweet,
                                  tweeter,
                                  lang,
                                  latitude,
                                  longitude))

                try:
                    Temptweets.insert(tweet_id=tweet_id,
                                      tweet_datetime=tweet_datetime,
                                      tweet_keyword=tweet_keyword,
                                      tweet=tweet, tweeter=tweeter,
                                      lang=lang, latitude=latitude,
                                      longitude=longitude).execute()
                except:
                    print("## Error: {} ##".format(sys.exc_info()))
    copy_tweets()


def copy_tweets():
    try:
        saved_tweet_ids = (Tweets
                           .select(Tweets.tweet_id)
                           .distinct())

        temp_tweets_ids = (Temptweets
                           .select(Temptweets.tweet_id)
                           .distinct())

        new_tweet_ids = (temp_tweets_ids - saved_tweet_ids)

        new_tweets = (Temptweets
                      .select(Temptweets.tweet_id,
                              Temptweets.tweet_datetime,
                              Temptweets.tweet_keyword,
                              Temptweets.tweet,Temptweets.tweeter,
                              Temptweets.lang, Temptweets.latitude,
                              Temptweets.longitude)
                       .where(Temptweets.tweet_id << new_tweet_ids))

        Tweets.insert_from([Tweets.tweet_id, Tweets.tweet_datetime,
                            Tweets.tweet_keyword, Tweets.tweet,
                            Tweets.tweeter, Tweets.lang, Tweets.latitude,
                            Tweets.longitude],new_tweets).execute()

    except:
        print("~~ Error: {} ~~".format(sys.exc_info()))

    db.execute_sql("truncate table temptweets")


#  Bring Calibretto to life
if __name__ == "__main__":
    initialize()
    get_tweets()
