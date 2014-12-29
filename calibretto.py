#!/usr/bin/env /usr/local/bin/python2.7

import twitter
import psycopg2
import sys

# Twitter authentication
# Grab your creds at https://apps.twitter.com

CONSUMER_KEY = '{Consumer Key (API Key)}'
CONSUMER_SECRET = '{Consumer Secret (API Secret)}'
OAUTH_TOKEN = '{Access Token}'
OAUTH_TOKEN_SECRET = '{Access Token Secret}'

auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

twitter_api = twitter.Twitter(domain='api.twitter.com', api_version='1.1', auth=auth)

# Connect to your PostgreSQL database
conn = psycopg2.connect(database="{database}", host="{host}", port="{port}", user="{username}", password="{password}")
cur = conn.cursor()

# Choose keywords
harvest_list = ['{keyword1}','{keyword2}']

# Create BatchID
cur.execute("select max(coalesce(batchid,0)) from tweetlog")
batch_id_cur = cur.fetchall()
if batch_id_cur[0][0] is None:
    batch_id = 0
else:
    batch_id = batch_id_cur[0][0]+1


# Given a keyword, perform harvest
for tweet_keyword in harvest_list: 

        # Truncate temp table
        cur.execute("""truncate temptweets""")
        conn.commit()

        # Perform search with given criteria
        search_results = twitter_api.search.tweets(q=tweet_keyword, count=100)

        # Set up each tweet as a status
        for status in search_results['statuses']:
            
            # Only return information for tweets with geo info
            if status["geo"]:

                # Create variables
                tweet_id = status['id_str']
                tweet_datetime = status["created_at"]
                tweet = status["text"]
                tweeter = "@" + status['user']['screen_name']
                lang = status['metadata']['iso_language_code']
                latitude = status["geo"]["coordinates"][0]
                longitude = status["geo"]["coordinates"][1]

                # Print a nice readout of each tweet
                print "     tweet_id: ",tweet_id,"\n"
                print "     tweet_datetime: ",tweet_datetime,"\n"
                print "     tweet_keyword: ",tweet_keyword,"\n"
                print "     tweet: ",tweet.encode('utf-8'),"\n"
                print "     tweeter: ",tweeter,"\n"
                print "     lang: ",lang,"\n"
                print "     latitude: ",latitude,"\n"
                print "     longitude: ",longitude,"\n"
                print "     #######################","\n"

                # Attempt to place tweets into temp table
                try:    
                    cur.execute("""insert into temptweets (tweet_id, tweet_datetime, tweet_keyword, tweet, tweeter, lang, latitude, longitude)
                                values (%s, %s, %s, %s, %s, %s, %s, %s);""",
                                (tweet_id, tweet_datetime, tweet_keyword, tweet.encode('utf-8'), tweeter, lang, latitude, longitude)
								) 
                # If there is an error, print the error type and skip tweet
                except:
                    print "############### Error:", sys.exc_info()[0], "###############"

        # Move new tweets into tweet table
        cur.execute("""insert into tweets (tweet_id, tweet_datetime, tweet_keyword, tweet, tweeter, lang, latitude, longitude)
        select * from temptweets where tweet_id NOT in
        (select distinct tweet_id from tweets)""")

        # Truncate temp table
        cur.execute("""truncate temptweets""")

        # Log batch with details
        cur.execute("""insert into tweetlog (BatchId, keyword, RunDate, HarvestedThisRun, TotalHarvested) values
        (
        '"""+str(batch_id)+"""',
        '"""+str(tweet_keyword)+"""',
        current_timestamp,
        ((select count(*) from tweets where tweet_keyword = '"""+str(tweet_keyword)+"""') - (select coalesce(TotalHarvested,0) from tweetlog where keyword = '"""+str(tweet_keyword)+"""' order by RunDate desc limit 1)),
        (select count(*) from tweets where tweet_keyword = '"""+str(tweet_keyword)+"""')
        )""")

        # Make the changes to the database persistent
        conn.commit()

