import psycopg2.extras

from features_impl.FeaturesImpl import *
from create_testtrain_dataset.MsgAnalysisResult import *

switch_to_trolls = True


def run_message_analysis(cursor, map_tweetid_to_result, query_user_in):
    if switch_to_trolls:
        query = 'SELECT tweet_id, tweet_text, urls, hashtags_count, user_mentions_count, like_count, tweet_client_name, CAST(r_user_followers_count as float) / CAST(r_user_friends_count + 1 as float) as RetweetedRatio FROM tweets WHERE tweet_language = \'en\' and user_id in' + query_user_in
    else:
        query = 'SELECT id_str, text, urls, hashtags_count, user_mentions_count, favorite_count, source, CAST(r_user_followers_count AS float) / CAST(r_user_friends_count + 1 AS float) as RetweetedRatio FROM tweets_n WHERE lang = \'en\' and user_id_str in' + query_user_in
        # query = 'SELECT id_str, text, urls, hashtags_count, user_mentions_count, favorite_count, source, CAST(r_user_followers_count AS float) / CAST(r_user_friends_count + 1 AS float) as RetweetedRatio FROM tweets_n WHERE lang = \'en\''

    cursor.execute(query)

    blobber = Blobber(analyzer=NaiveBayesAnalyzer())
    for row in cursor:
        tweet_id = row[0]
        tweet_text = row[1]
        urls = row[2]
        hashtags_count = row[3]
        user_mentions_count = row[4]
        favorite_count = row[5]
        tweet_client_name = row[6]
        retweeted_user_ratio = row[7]

        chars_number, words_number, polarity, subjectivity, tag = analyse_tweet_text(tweet_text, blobber)
        tweet_client_category = assign_category_to_twitter_client(tweet_client_name)
        portals_in_tweet = parse_urls_from_db(urls)
        url_portal_category = check_portals_category(portals_in_tweet)

        tweet = map_tweetid_to_result[str(tweet_id)]
        tweet.set_text_analysis_results(chars_number, words_number, polarity, subjectivity, tag, hashtags_count, user_mentions_count)
        tweet.set_favorite_count(favorite_count)
        tweet.set_tweet_client_name_and_category(tweet_client_name, tweet_client_category)
        tweet.set_url_analysis_result(portals_in_tweet, url_portal_category)
        if retweeted_user_ratio is not None:
            tweet.set_retweeted_user_ratio(retweeted_user_ratio)
        else:
            tweet.set_retweeted_user_ratio(-1.0)


def run_tweeting_time_analyses(cursor, map_tweetid_to_result, map_user_to_tweets, query_user_in):
    if switch_to_trolls:
        query = 'select user_id, tweet_time, tweet_id from tweets where user_id in ' + query_user_in + ' group by user_id, tweet_time, tweet_id order by tweet_time'
    else:
        query = 'select user_id_str, created_at, id_str from tweets_n where user_id_str in ' + query_user_in + ' group by user_id_str, created_at, id_str order by created_at'
        # query = 'select user_id_str, created_at, id_str from tweets_n group by user_id_str, created_at, id_str order by created_at'

    cursor.execute(query)

    data = []
    users_tweets_timestamps = {}

    for row in cursor:
        user_id = row[0]
        tweet_date = row[1]
        data.append([user_id, tweet_date.timestamp()])
        users_tweets_timestamps[user_id] = []

    for elem in data:
        users_tweets_timestamps[elem[0]].append(elem[1])

    del data

    # first analysis, tweets series
    results_tweets_series = analyse_tweets_series_with_time_gaps(users_tweets_timestamps, time_window_minutes=15, number_of_top_series_to_avg=5)
    for result in results_tweets_series:
        user_id = result[0]
        max_serie_size = result[1]
        top_n_series_avg = result[2]

        for tweet_id in map_user_to_tweets[user_id]:
            map_tweetid_to_result[tweet_id].set_tweet_series_analysis_results(max_serie_size, top_n_series_avg)

    # second analysis, max tweets number in time window
    results_max_tweets_in_time_window = max_messages_number_in_time_window(users_tweets_timestamps)
    for result in results_max_tweets_in_time_window:
        user_id = result[0]
        max_tweets_in_time_window = result[1]

        for tweet_id in map_user_to_tweets[user_id]:
            map_tweetid_to_result[tweet_id].set_max_tweets_number_in_time_window(max_tweets_in_time_window)


def run_tweeting_frequency_analysis(cursor, map_tweetid_to_result, map_user_to_tweets, query_user_in):
    if switch_to_trolls:
        query = 'SELECT user_id, days_active::float8 / tweets_number::float8 as tweeting_frequency FROM (SELECT user_id, account_creation_date, count(*) as tweets_number, date(max(tweet_time)) - account_creation_date as days_active FROM tweets WHERE user_id in ' + query_user_in + ' GROUP BY user_id, account_creation_date) as i'
    else:
        query = 'SELECT user_id_str, days_active::float8 / tweets_number::float8 as tweeting_frequency FROM (SELECT user_id_str, count(*) as tweets_number, date(max(created_at)) - date(user_created_at) as days_active FROM tweets_n WHERE user_id_str in ' + query_user_in + ' GROUP BY user_id_str, user_created_at) as i'

    map_usr_id_to_tweeting_freq = {}
    cursor.execute(query)
    for row in cursor:
        user_id = row[0]
        tweeting_frequency = row[1]

        map_usr_id_to_tweeting_freq[user_id] = tweeting_frequency

    for user_id, tweeting_frequency in map_usr_id_to_tweeting_freq.items():
        for tweet_id in map_user_to_tweets[user_id]:
            map_tweetid_to_result[tweet_id].set_tweeting_frequency(tweeting_frequency)

    del map_usr_id_to_tweeting_freq


def run_users_analysis(cursor, map_tweetid_to_result, map_user_to_tweets, query_user_in):
    if switch_to_trolls:
        query = 'SELECT user_id, follower_count, following_count FROM tweets WHERE user_id in ' + query_user_in
    else:
        # query = 'SELECT user_id_str, user_followers_count, user_friends_count FROM tweets_n WHERE user_id_str in ' + query_user_in
        query = 'SELECT user_id_str, max(user_followers_count) as user_followers_count, max(user_friends_count) as user_friends_count FROM tweets_n WHERE user_id_str in' + query_user_in + ' GROUP BY user_id_str'
        # query = 'SELECT user_id_str, user_followers_count, user_friends_count FROM tweets_n'

    map_user_id_to_result = {}
    cursor.execute(query)
    for row in cursor:
        user_id = row[0]
        follower_count = row[1]
        following_count = row[2]
        ratio_follower_following = calculate_ratio_follower_following(follower_count, following_count)

        map_user_id_to_result[user_id] = (follower_count, following_count, ratio_follower_following)

    for user_id, result_tuple in map_user_id_to_result.items():
        for tweet_id in map_user_to_tweets[user_id]:
            map_tweetid_to_result[tweet_id].set_user_data(result_tuple[0], result_tuple[1], result_tuple[2])

    del map_user_id_to_result


def run_message_similarity_analysis(cursor, map_tweetid_to_result, query_user_in):
    if switch_to_trolls:
        query = 'SELECT user_id, tweet_id, tweet_text FROM tweets WHERE tweet_language = \'en\' and user_id in' + query_user_in
    else:
        query = 'SELECT user_id_str, id_str, text FROM tweets_n WHERE lang = \'en\' and user_id_str in' + query_user_in
        # query = 'SELECT user_id_str, id_str, text FROM tweets_n WHERE lang = \'en\''

    cursor.execute(query)

    perform_message_similarity_analysis(cursor, map_tweetid_to_result, 0.8)


# TODO czy tutaj analizowac tylko eng, zmieniam na all
def run_user_favorite_client_analysis(cursor, map_tweetid_to_result, map_user_to_tweets, query_user_in):
    if switch_to_trolls:
        # query = 'SELECT a.user_id, a.tweet_client_name, a.count FROM (select user_id, tweet_client_name, count(*) as count from tweets where tweet_language =\'en\' group by user_id, tweet_client_name) as a INNER JOIN (SELECT user_id, MAX(count) count FROM (select user_id, count(*) as count from tweets where tweet_language =\'en\' group by user_id, tweet_client_name) as aa GROUP BY user_id) b ON a.user_id = b.user_id AND a.count = b.count WHERE a.user_id in' + query_user_in
        query = 'SELECT a.user_id, a.tweet_client_name, a.count FROM (select user_id, tweet_client_name, count(*) as count from tweets group by user_id, tweet_client_name) as a INNER JOIN (SELECT user_id, MAX(count) count FROM (select user_id, count(*) as count from tweets group by user_id, tweet_client_name) as aa GROUP BY user_id) b ON a.user_id = b.user_id AND a.count = b.count WHERE a.user_id in' + query_user_in
    else:
        # query = 'SELECT a.user_id_str, a.source, a.count FROM (select user_id_str, source, count(*) as count from tweets_n where lang = \'en\' group by user_id_str, source) as a INNER JOIN (SELECT user_id_str, MAX(count) count FROM (select user_id_str, count(*) as count from tweets_n where lang = \'en\' group by user_id_str, source) as aa GROUP BY user_id_str) b ON a.user_id_str = b.user_id_str AND a.count = b.count WHERE a.user_id_str in' + query_user_in

        query = 'SELECT a.user_id_str, a.source, a.count FROM (select user_id_str, source, count(*) as count from tweets_n group by user_id_str, source) as a INNER JOIN (SELECT user_id_str, MAX(count) count FROM (select user_id_str, count(*) as count from tweets_n group by user_id_str, source) as aa GROUP BY user_id_str) b ON a.user_id_str = b.user_id_str AND a.count = b.count WHERE a.user_id_str in' + query_user_in
        # query = 'SELECT a.user_id_str, a.source, a.count FROM (select user_id_str, source, count(*) as count from tweets_n group by user_id_str, source) as a INNER JOIN (SELECT user_id_str, MAX(count) count FROM (select user_id_str, count(*) as count from tweets_n group by user_id_str, source) as aa GROUP BY user_id_str) b ON a.user_id_str = b.user_id_str AND a.count = b.count'

    cursor.execute(query)

    map_user_id_to_result = get_user_favorite_client_category_and_clients(cursor)

    for user_id, result_tuple in map_user_id_to_result.items():
        for tweet_id in map_user_to_tweets[user_id]:
            map_tweetid_to_result[tweet_id].set_favorite_client_analysis_result(result_tuple[0], result_tuple[1])


def run_graph_analysis(cursor, map_tweetid_to_result, map_user_to_tweets):
    retweets_number_above = 2
    # when changing this to zero, change default value in result class to 1
    min_clique_size_to_count = 3

    results = perfmorm_graph_analysis_on_retweeted_users(cursor, map_user_to_tweets, switch_to_trolls, retweets_number_above, min_clique_size_to_count)

    for user_id, data in results.items():
        max_clique_size = data['maxCliqueSize']
        number_of_cliques_in = data['numberOfCliquesIn']

        for tweet_id in map_user_to_tweets[user_id]:
            map_tweetid_to_result[tweet_id].set_graph_analysis_result(max_clique_size, number_of_cliques_in)


def get_choosen_users_tweets_ids(query_user_in_part, tweet_and_metrics):
    if switch_to_trolls:
        query = 'SELECT user_id, tweet_id FROM tweets WHERE tweet_language = \'en\' AND user_id in ' + query_user_in_part
        label = "UNWANTED"
    else:
        query = 'SELECT user_id_str, id_str FROM tweets_n WHERE lang = \'en\' AND user_id_str in ' + query_user_in_part
        # query = 'SELECT user_id_str, id_str FROM tweets_n WHERE lang = \'en\''

        label = "NORMAL"

    connection = psycopg2.connect("dbname=twitter-us-election user=postgres password=1234")
    cursor = connection.cursor()
    cursor.execute(query)

    map_user_to_tweets = {}

    for row in cursor:
        user_id = row[0]
        tweet_id = row[1]
        tweet_and_metrics[tweet_id] = AnalysisResult(user_id, tweet_id, label)
        append_to_user_tweet_map(user_id, tweet_id, map_user_to_tweets)

    return map_user_to_tweets


def append_to_user_tweet_map(user_id, tweet_id, map_user_to_tweets):
    if user_id not in map_user_to_tweets:
        map_user_to_tweets[user_id] = []

    map_user_to_tweets[user_id].append(tweet_id)


def prepare_for_analysis(user_ids_file):
    f = open(user_ids_file, "r")

    query_user_in = "("
    for user_id in f:
        query_user_in += "'" + str(user_id).rstrip() + "', "
    query_user_in = query_user_in[:-2] + ")"

    f.close()

    tweetsid_and_metrics = {}
    map_user_to_tweets = get_choosen_users_tweets_ids(query_user_in, tweetsid_and_metrics)

    return tweetsid_and_metrics, query_user_in, map_user_to_tweets


def convert_to_weka_file(map_tweetid_to_result, out_file_name):
    with open(out_file_name, 'a', encoding="utf-8") as the_file:
        for elem in list(map_tweetid_to_result.values()):
            the_file.write(elem.convert_to_weka_data_row_format() + "\n")


def perform_analyses(user_ids_file, out_file_name):
    map_tweetid_to_result, query_user_in, map_user_to_tweets = prepare_for_analysis(user_ids_file)

    connection = psycopg2.connect("dbname=twitter-us-election user=postgres password=1234")
    cursor = connection.cursor()

    run_message_analysis(cursor, map_tweetid_to_result, query_user_in)
    print("DONE msg")
    run_graph_analysis(cursor, map_tweetid_to_result, map_user_to_tweets)
    print("DONE graph")
    run_tweeting_time_analyses(cursor, map_tweetid_to_result, map_user_to_tweets, query_user_in)
    print("DONE time")
    run_users_analysis(cursor, map_tweetid_to_result, map_user_to_tweets, query_user_in)
    print("DONE users")
    run_user_favorite_client_analysis(cursor, map_tweetid_to_result, map_user_to_tweets, query_user_in)
    print("DONE favclient")
    run_message_similarity_analysis(cursor, map_tweetid_to_result, query_user_in)
    print("DONE similarity")

    convert_to_weka_file(map_tweetid_to_result, out_file_name)


if __name__ == '__main__':
    # user_ids_file = "users_set_from_ira"
    # out_file_name = 'new-users-data-ira-out2807new.txt'
    # perform_analyses(user_ids_file, out_file_name)

    user_ids_file = "C:\\Users\\Lukas\\PycharmProjects\\tweetsApp\\operationsonfinaldataset\\refactored\\usersHpart1"
    out_file_name = 'users-data-harvard-out-part1.txt'
    perform_analyses(user_ids_file, out_file_name)

    user_ids_file = "C:\\Users\\Lukas\\PycharmProjects\\tweetsApp\\operationsonfinaldataset\\refactored\\usersHpart1a"
    out_file_name = 'users-data-harvard-out-part2.txt'
    perform_analyses(user_ids_file, out_file_name)

    user_ids_file = "C:\\Users\\Lukas\\PycharmProjects\\tweetsApp\\operationsonfinaldataset\\refactored\\usersHpart2"
    out_file_name = 'users-data-harvard-out-part3.txt'
    perform_analyses(user_ids_file, out_file_name)

    user_ids_file = "C:\\Users\\Lukas\\PycharmProjects\\tweetsApp\\operationsonfinaldataset\\refactored\\usersHpart2a"
    out_file_name = 'users-data-harvard-out-part4.txt'
    perform_analyses(user_ids_file, out_file_name)

    user_ids_file = "C:\\Users\\Lukas\\PycharmProjects\\tweetsApp\\operationsonfinaldataset\\refactored\\usersHpart3"
    out_file_name = 'users-data-harvard-out-part5.txt'
    perform_analyses(user_ids_file, out_file_name)

    user_ids_file = "C:\\Users\\Lukas\\PycharmProjects\\tweetsApp\\operationsonfinaldataset\\refactored\\usersHpart3a"
    out_file_name = 'users-data-harvard-out-part6.txt'
    perform_analyses(user_ids_file, out_file_name)
