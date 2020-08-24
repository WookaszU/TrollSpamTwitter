import time
import psycopg2.extras
import tweepy
from tweepy import RateLimitError


def count_elements_from_string_list(list_string):
    list_string = list_string[1:-1]
    splitted = list_string.split(",")
    if splitted[0] == '':
        quantity = 0
    else:
        quantity = len(splitted)

    return quantity


def add_data_counters_values():
    connection = psycopg2.connect("dbname=twitter-us-election user=postgres password=1234")
    cursor = connection.cursor()
    query = 'SELECT id, hashtags, urls, user_mentions, hashtags_count, user_mentions_count, urls_count FROM tweets'
    cursor.execute(query)

    update_rows = set()

    for row in cursor:
        id = row[0]

        hashtags = row[1]
        urls = row[2]
        user_mentions = row[3]

        hashtags_number = count_elements_from_string_list(hashtags)
        urls_number = count_elements_from_string_list(urls)
        user_mentions_number = count_elements_from_string_list(user_mentions)

        update_rows.add((hashtags_number, user_mentions_number, urls_number, id))

    print('inserting')

    update_query = """UPDATE tweets AS t 
                          SET hashtags_count = e.hashtags_count, user_mentions_count = e.user_mentions_count, urls_count = e.urls_count
                          FROM (VALUES %s) AS e(hashtags_count, user_mentions_count, urls_count, id) 
                          WHERE e.id = t.id;"""

    psycopg2.extras.execute_values(
        cursor, update_query, update_rows, template=None, page_size=100
    )

    connection.commit()
    connection.close()


def prepare_twitter_api_connection():
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

    return api


def update_ira_with_retweeted_users_details():
    pass


def call_twitter_for_users_data(users_ids):
    users = []
    done = False
    while not done:
        try:
            users = api.lookup_users(users_ids)
            done = True
        except RateLimitError:
            time.sleep(10)

    return users


def update_rows_with_data_from_twitter_api(update_rows_with_data_from_twitter):
    rows_ids = []
    users_ids = []

    update_rows = set()
    for elem in update_rows_with_data_from_twitter:
        rows_ids.append(elem[0])
        users_ids.append(elem[1])

        if len(users_ids) >= 100:
            users_data = call_twitter_for_users_data(users_ids)

            i = 0
            for data in users_data:
                while users_ids[i] != data.id_str:
                    i += 1

                update_rows.add((data.created_at,
                                 data.description,
                                 data.followers_count,
                                 data.friends_count,
                                 data.location,
                                 data.lang,
                                 data.statuses_count,
                                 rows_ids[i])
                                )
            rows_ids = []
            users_ids = []

    file_name = 'copy-of-data-downloaded-user-v2.txt'
    with open(file_name, 'a', encoding="utf-8") as the_file:
        the_file.write("\n".join(str(item) for item in update_rows))

    print("inserting to database.")

    update_query = """UPDATE tweets AS t
                              SET r_user_created_at = e.created_at, r_user_description = e.description, r_user_followers_count = e.followers_count, r_user_friends_count = e.friends_count, r_user_location = e.location, r_user_lang = e.lang, r_user_statuses_count = e.statuses_count
                              FROM (VALUES %s) AS e(created_at, description, followers_count, friends_count, location, lang, statuses_count, id)
                              WHERE e.id = t.id;"""

    psycopg2.extras.execute_values(
        cursor, update_query, update_rows, template=None, page_size=100
    )

    connection.commit()
    connection.close()


if __name__ == '__main__':
    # api = prepare_twitter_api_connection()

    connection = psycopg2.connect("dbname=twitter-us-election user=postgres password=1234")
    cursor = connection.cursor()
    query = 'SELECT id, retweet_user_id FROM tweets WHERE retweet_user_id != \'\''
    cursor.execute(query)

    update_rows_with_data_from_twitter = set()
    update_rows_with_data_from_ira = set()

    for row in cursor:
        db_id = row[0]
        retweet_user_id = row[1]

        if len(retweet_user_id) == 64:
            update_rows_with_data_from_ira.add((db_id, retweet_user_id))
        else:
            update_rows_with_data_from_twitter.add((db_id, retweet_user_id))

    users_ids = [x[1] for x in update_rows_with_data_from_ira]

    query_user_in = "("
    for user_id in users_ids:
        query_user_in += "'" + str(user_id).rstrip() + "', "
    query_user_in = query_user_in[:-2] + ")"

    # query = 'SELECT account_creation_date, user_profile_description, follower_count, following_count, user_reported_location, account_language, count_result.r_user_statuses_count, t.user_id FROM tweets t INNER JOIN (SELECT user_id, count(*) as r_user_statuses_count FROM tweets GROUP BY user_id) count_result ON count_result.user_id = t.user_id WHERE t.user_id in' + query_user_in + ' GROUP BY account_creation_date, user_profile_description, follower_count, following_count, user_reported_location, account_language, count_result.r_user_statuses_count, t.user_id;'
    query = 'SELECT account_creation_date, user_profile_description, follower_count, following_count, user_reported_location, account_language, count_result.r_user_statuses_count, t.user_id FROM tweets t INNER JOIN (SELECT user_id, count(*) as r_user_statuses_count FROM tweets GROUP BY user_id) count_result ON count_result.user_id = t.user_id GROUP BY account_creation_date, user_profile_description, follower_count, following_count, user_reported_location, account_language, count_result.r_user_statuses_count, t.user_id;'

    cursor.execute(query)

    map_usr_id_to_details = {}
    for row in cursor:
        map_usr_id_to_details[row[7]] = [row[0],
                                         row[1],
                                         row[2],
                                         row[3],
                                         row[4],
                                         row[5],
                                         row[6]]

    update_rows = set()
    for (db_id, retweet_user_id) in update_rows_with_data_from_ira:
        if retweet_user_id in map_usr_id_to_details:
            data_to_insert_to_row = map_usr_id_to_details[retweet_user_id]
            to_insert = data_to_insert_to_row.copy()
            to_insert.append(db_id)
            update_rows.add(tuple(to_insert))

    print("inserting to database.")

    update_query = """UPDATE tweets AS t
                              SET r_user_created_at = e.created_at, r_user_description = e.description, r_user_followers_count = e.followers_count, r_user_friends_count = e.friends_count, r_user_location = e.location, r_user_lang = e.lang, r_user_statuses_count = e.statuses_count
                              FROM (VALUES %s) AS e(created_at, description, followers_count, friends_count, location, lang, statuses_count, id)
                              WHERE e.id = t.id;"""

    psycopg2.extras.execute_values(
        cursor, update_query, update_rows, template=None, page_size=100
    )

    connection.commit()
    connection.close()
