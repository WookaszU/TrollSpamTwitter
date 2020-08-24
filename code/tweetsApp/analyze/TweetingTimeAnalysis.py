import psycopg2.extras
from features_impl.FeaturesImpl import max_messages_number_in_time_window, analyse_tweets_series_with_time_gaps


def append_to_bin(value, bins_numbers_list, bins):
    pointer = 0
    epsilon = 0.00000000000000001
    while value - bins_numbers_list[pointer] > epsilon:
        pointer += 1

    bins[pointer] += 1

    return pointer


def append_all_to_bins(tweets_info, file_name):
    bins_numbers_list = list(range(1, 101))
    bins_numbers_list.extend([200, 300, 400, 500, 9999])
    bins_serie_max_len = len(bins_numbers_list) * [0]
    bins_n_series_avg = len(bins_numbers_list) * [0]

    for info in tweets_info:
        append_to_bin(info[1], bins_numbers_list, bins_serie_max_len)
        append_to_bin(info[2], bins_numbers_list, bins_n_series_avg)

    with open(file_name, 'a') as the_file:
        the_file.write("\n".join(str(item) for item in bins_serie_max_len))
        the_file.write("\n------------------\n")
        the_file.write("\n------------------\n")
        the_file.write("\n".join(str(item) for item in bins_n_series_avg))


def append_max_tweets_to_bins(tweets_info, file_name):
    bins_numbers_list = list(range(1, 101))
    bins_numbers_list.extend([200, 300, 400, 500, 9999])
    bins_max_tweets = len(bins_numbers_list) * [0]

    for info in tweets_info:
        append_to_bin(info[1], bins_numbers_list, bins_max_tweets)

    with open(file_name, 'a') as the_file:
        the_file.write("\n".join(str(item) for item in bins_max_tweets))
        the_file.write("\n------------------\n")


if __name__ == '__main__':
    connection = psycopg2.connect("dbname=twitter-us-election user=postgres password=1234")
    cursor = connection.cursor()

    # with retweets
    # query = 'select user_id, tweet_time, tweet_id from tweets group by user_id, tweet_time, tweet_id order by tweet_time'
    query = 'select user_id_str, created_at, id_str from tweets_n group by user_id_str, created_at, id_str order by created_at'

    # without retweets
    # query = 'select user_id, tweet_time, tweet_id from tweets where is_retweet is false group by user_id, tweet_time, tweet_id order by tweet_time'
    # query = 'select user_id_str, created_at, id_str from tweets_n where r_created_at is null group by user_id_str, created_at, id_str order by created_at'

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

    # results_max_window_msgs = max_messages_number_in_time_window(users_tweets_timestamps)
    results = analyse_tweets_series_with_time_gaps(users_tweets_timestamps, 15, 5)

    file_name = 'series-tweets-5m-ira.txt'
    append_all_to_bins(results, file_name)
    # append_max_tweets_to_bins(results_max_window_msgs, file_name)