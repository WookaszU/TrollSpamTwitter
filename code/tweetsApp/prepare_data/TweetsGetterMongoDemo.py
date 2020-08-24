import json

import psycopg2
import psycopg2.extras
import tweepy
from pymongo import MongoClient


def get_tweet_by_id(id_of_tweet):
    tweet = api.get_status(id_of_tweet)

    created_at = tweet.created_at
    hashtags = json.dumps(tweet.entities['hashtags'])
    symbols = json.dumps(tweet.entities['symbols'])
    user_mentions = json.dumps(tweet.entities['user_mentions'])
    urls = json.dumps(tweet.entities['urls'])

    hashtags_count = len(tweet.entities['hashtags'])
    symbols_count = len(tweet.entities['symbols'])
    user_mentions_count = len(tweet.entities['user_mentions'])
    urls_count = len(tweet.entities['urls'])

    favorite_count = tweet.favorite_count
    id_str = tweet.id_str
    in_reply_to_status_id_str = tweet.in_reply_to_status_id_str
    in_reply_to_user_id_str = tweet.in_reply_to_user_id_str
    is_quote_status = tweet.is_quote_status

    lang = tweet.lang
    place = tweet.place
    coordinates = tweet.coordinates
    retweet_count = tweet.retweet_count
    retweeted = tweet.retweeted
    source = tweet.source
    text = tweet.text
    truncated = tweet.truncated

    user_created_at = tweet.user.created_at
    user_default_profile = tweet.user.default_profile
    user_description = tweet.user.description
    user_favourites_count = tweet.user.favourites_count
    user_followers_count = tweet.user.followers_count
    user_friends_count = tweet.user.friends_count
    user_has_extended_profile = tweet.user.has_extended_profile
    user_id_str = tweet.user.id_str
    user_lang = tweet.user.lang
    user_location = tweet.user.location
    user_statuses_count = tweet.user.statuses_count
    user_verified = tweet.user.verified

    q_created_at = None
    q_hashtags = None
    q_symbols = None
    q_user_mentions = None
    q_urls = None
    q_hashtags_count = None
    q_symbols_count = None
    q_user_mentions_count = None
    q_urls_count = None
    q_favorite_count = None
    q_id_str = None
    q_is_quote_status = None
    q_lang = None
    q_place = None
    q_coordinates = None
    q_retweet_count = None
    q_retweeted = None
    q_source = None
    q_text = None
    q_truncated = None
    q_user_created_at = None
    q_user_default_profile = None
    q_user_description = None
    q_user_favourites_count = None
    q_user_followers_count = None
    q_user_friends_count = None
    q_user_has_extended_profile = None
    q_user_id_str = None
    q_user_lang = None
    q_user_location = None
    q_user_statuses_count = None
    q_user_verified = None
    r_created_at = None
    r_hashtags = None
    r_symbols = None
    r_user_mentions = None
    r_urls = None
    r_hashtags_count = None
    r_symbols_count = None
    r_user_mentions_count = None
    r_urls_count = None
    r_favorite_count = None
    r_id_str = None
    r_is_quote_status = None
    r_lang = None
    r_place = None
    r_coordinates = None
    r_retweet_count = None
    r_retweeted = None
    r_source = None
    r_text = None
    r_truncated = None
    r_user_created_at = None
    r_user_default_profile = None
    r_user_description = None
    r_user_favourites_count = None
    r_user_followers_count = None
    r_user_friends_count = None
    r_user_has_extended_profile = None
    r_user_id_str = None
    r_user_lang = None
    r_user_location = None
    r_user_statuses_count = None
    r_user_verified = None

    if hasattr(tweet, 'quoted_status'):
        q_created_at = tweet.quoted_status.created_at
        q_hashtags = json.dumps(tweet.quoted_status.entities['hashtags'])
        q_symbols = json.dumps(tweet.quoted_status.entities['symbols'])
        q_user_mentions = json.dumps(tweet.quoted_status.entities['user_mentions'])
        q_urls = json.dumps(tweet.quoted_status.entities['urls'])

        q_hashtags_count = len(tweet.quoted_status.entities['hashtags'])
        q_symbols_count = len(tweet.quoted_status.entities['symbols'])
        q_user_mentions_count = len(tweet.quoted_status.entities['user_mentions'])
        q_urls_count = len(tweet.quoted_status.entities['urls'])

        q_favorite_count = tweet.quoted_status.favorite_count
        q_id_str = tweet.quoted_status.id_str
        q_is_quote_status = tweet.quoted_status.is_quote_status

        q_lang = tweet.quoted_status.lang
        q_place = tweet.quoted_status.place
        q_coordinates = tweet.quoted_status.coordinates
        q_retweet_count = tweet.quoted_status.retweet_count
        q_retweeted = tweet.quoted_status.retweeted
        q_source = tweet.quoted_status.source
        q_text = tweet.quoted_status.text
        q_truncated = tweet.quoted_status.truncated

        q_user_created_at = tweet.quoted_status.user.created_at
        q_user_default_profile = tweet.quoted_status.user.default_profile
        q_user_description = tweet.quoted_status.user.description
        q_user_favourites_count = tweet.quoted_status.user.favourites_count
        q_user_followers_count = tweet.quoted_status.user.followers_count
        q_user_friends_count = tweet.quoted_status.user.friends_count
        q_user_has_extended_profile = tweet.quoted_status.user.has_extended_profile
        q_user_id_str = tweet.quoted_status.user.id_str
        q_user_lang = tweet.quoted_status.user.lang
        q_user_location = tweet.quoted_status.user.location
        q_user_statuses_count = tweet.quoted_status.user.statuses_count
        q_user_verified = tweet.quoted_status.user.verified

    if hasattr(tweet, 'retweeted_status'):
        r_created_at = tweet.retweeted_status.created_at
        r_hashtags = json.dumps(tweet.retweeted_status.entities['hashtags'])
        r_symbols = json.dumps(tweet.retweeted_status.entities['symbols'])
        r_user_mentions = json.dumps(tweet.retweeted_status.entities['user_mentions'])
        r_urls = json.dumps(tweet.retweeted_status.entities['urls'])

        r_hashtags_count = len(tweet.retweeted_status.entities['hashtags'])
        r_symbols_count = len(tweet.retweeted_status.entities['symbols'])
        r_user_mentions_count = len(tweet.retweeted_status.entities['user_mentions'])
        r_urls_count = len(tweet.retweeted_status.entities['urls'])

        r_favorite_count = tweet.retweeted_status.favorite_count
        r_id_str = tweet.retweeted_status.id_str
        r_is_quote_status = tweet.retweeted_status.is_quote_status

        r_lang = tweet.retweeted_status.lang
        r_place = tweet.retweeted_status.place
        r_coordinates = tweet.retweeted_status.coordinates
        r_retweet_count = tweet.retweeted_status.retweet_count
        r_retweeted = tweet.retweeted_status.retweeted
        r_source = tweet.retweeted_status.source
        r_text = tweet.retweeted_status.text
        r_truncated = tweet.retweeted_status.truncated

        r_user_created_at = tweet.retweeted_status.user.created_at
        r_user_default_profile = tweet.retweeted_status.user.default_profile
        r_user_description = tweet.retweeted_status.user.description
        r_user_favourites_count = tweet.retweeted_status.user.favourites_count
        r_user_followers_count = tweet.retweeted_status.user.followers_count
        r_user_friends_count = tweet.retweeted_status.user.friends_count
        r_user_has_extended_profile = tweet.retweeted_status.user.has_extended_profile
        r_user_id_str = tweet.retweeted_status.user.id_str
        r_user_lang = tweet.retweeted_status.user.lang
        r_user_location = tweet.retweeted_status.user.location
        r_user_statuses_count = tweet.retweeted_status.user.statuses_count
        r_user_verified = tweet.retweeted_status.user.verified

    connection = psycopg2.connect("dbname=twitter-us-election user=postgres password=1234")
    cursor = connection.cursor()
    cursor.execute('SELECT version()')
    db_version = cursor.fetchone()
    print(db_version)

    data = []
    row = created_at, hashtags, symbols, user_mentions, urls, hashtags_count, symbols_count, user_mentions_count, urls_count, favorite_count, id_str, in_reply_to_status_id_str, in_reply_to_user_id_str, is_quote_status, lang, place, coordinates, retweet_count, retweeted, source, text, truncated, user_created_at, user_default_profile, user_description, user_favourites_count, user_followers_count, user_friends_count, user_has_extended_profile, user_id_str, user_lang, user_location, user_statuses_count, user_verified, q_created_at, q_hashtags, q_symbols, q_user_mentions, q_urls, q_hashtags_count, q_symbols_count, q_user_mentions_count, q_urls_count, q_favorite_count, q_id_str, q_is_quote_status, q_lang, q_place, q_coordinates, q_retweet_count, q_retweeted, q_source, q_text, q_truncated, q_user_created_at, q_user_default_profile, q_user_description, q_user_favourites_count, q_user_followers_count, q_user_friends_count, q_user_has_extended_profile, q_user_id_str, q_user_lang, q_user_location, q_user_statuses_count, q_user_verified, r_created_at, r_hashtags, r_symbols, r_user_mentions, r_urls, r_hashtags_count, r_symbols_count, r_user_mentions_count, r_urls_count, r_favorite_count, r_id_str, r_is_quote_status, r_lang, r_place, r_coordinates, r_retweet_count, r_retweeted, r_source, r_text, r_truncated, r_user_created_at, r_user_default_profile, r_user_description, r_user_favourites_count, r_user_followers_count, r_user_friends_count, r_user_has_extended_profile, r_user_id_str, r_user_lang, r_user_location, r_user_statuses_count, r_user_verified
    data.append(row)
    data.append(row)

    insert_query = 'INSERT INTO tweets_normal (created_at, hashtags, symbols, user_mentions, urls, hashtags_count, symbols_count, user_mentions_count, urls_count, favorite_count, id_str, in_reply_to_status_id_str, in_reply_to_user_id_str, is_quote_status, lang, place, coordinates, retweet_count, retweeted, source, text, truncated, user_created_at, user_default_profile, user_description, user_favourites_count, user_followers_count, user_friends_count, user_has_extended_profile, user_id_str, user_lang, user_location, user_statuses_count, user_verified, q_created_at, q_hashtags, q_symbols, q_user_mentions, q_urls, q_hashtags_count, q_symbols_count, q_user_mentions_count, q_urls_count, q_favorite_count, q_id_str, q_is_quote_status, q_lang, q_place, q_coordinates, q_retweet_count, q_retweeted, q_source, q_text, q_truncated, q_user_created_at, q_user_default_profile, q_user_description, q_user_favourites_count, q_user_followers_count, q_user_friends_count, q_user_has_extended_profile, q_user_id_str, q_user_lang, q_user_location, q_user_statuses_count, q_user_verified, r_created_at, r_hashtags, r_symbols, r_user_mentions, r_urls, r_hashtags_count, r_symbols_count, r_user_mentions_count, r_urls_count, r_favorite_count, r_id_str, r_is_quote_status, r_lang, r_place, r_coordinates, r_retweet_count, r_retweeted, r_source, r_text, r_truncated, r_user_created_at, r_user_default_profile, r_user_description, r_user_favourites_count, r_user_followers_count, r_user_friends_count, r_user_has_extended_profile, r_user_id_str, r_user_lang, r_user_location, r_user_statuses_count, r_user_verified) VALUES %s'
    template = '(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'

    psycopg2.extras.execute_values(
        cursor, insert_query, data, template=template  # , page_size=150
    )

    connection.commit()

    print(tweet)


def get_tweets_with_ids(tweets_ids):
    # tweets_ids = ["1213514941958905857", "1213530379111583747", "795952587304529920"]
    tweets = api.statuses_lookup(tweets_ids)
    return tweets


def get_tweets_with_ids_as_json(tweets_ids):
    tweets = get_tweets_with_ids(tweets_ids)
    tweets_json = []
    for tt in tweets:
        tweets_json.append(tt._json)
    return tweets_json


def get_and_save_tweets(tweets_ids):
    client = MongoClient()
    db = client['tweets-election-day']
    tweets_collection = db.tweets

    tweets_json = get_tweets_with_ids_as_json(tweets_ids)
    if len(tweets_json) > 0:
        tweets_collection.insert_many(tweets_json)


# 100 tweets max per request via twitter api
def get_and_save_tweets_with_ids_from_file(file_path):
    with open(file_path) as fp:
        ids = []
        for line in fp:
            ids.append(line.rstrip())
            if len(ids) >= 100:
                print(ids[-1])
                get_and_save_tweets(ids)
                ids = []


if __name__ == '__main__':

    # Fill fields with twitter api key, secret, tokens
    CONSUMER_KEY = ""
    CONSUMER_SECRET = ""
    ACCESS_TOKEN = ""
    ACCESS_TOKEN_SECRET = ""

    # Authenticate to Twitter
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    api.verify_credentials()

    status = api.get_status('1287886038686474242')
    # user = api.get_user('1')

    file_path = 'data/election-day.txt'
    # get_and_save_tweets_with_ids_from_file(file_path)



    # get_tweet_by_id("1213593836846493696")
    # error ten na dole source duze
    # get_tweet_by_id("1213514941958905857")

    data = api.rate_limit_status()
    remaining = data['resources']['lists']['/lists/statuses']['remaining']
    print(remaining)

    # get_tweet_by_id("795952534565298177")
