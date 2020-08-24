from features_impl.FeaturesImpl import *
import psycopg2.extras
from statistics import mean
from textblob.sentiments import NaiveBayesAnalyzer
from textblob import Blobber

import sys
import os

from analyze.Utils import *

conf_path = os.getcwd()
sys.path.append(conf_path)
sys.path.append(conf_path + '\\refactored')


def append_to_bin(value, bins_numbers_list, bins):
    pointer = 0
    epsilon = 0.00000000000000001
    while value - bins_numbers_list[pointer] > epsilon:
        pointer += 1

    bins[pointer] += 1

    return pointer


def count_bins(tweets_info):
    bins_number_subjectivity = (0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 9999)
    bins_subject = len(bins_number_subjectivity) * [0]

    bins_number_polarity = (
        -1.0, -0.9, -0.8, -0.7, -0.6, -0.5, -0.4, -0.3, -0.2, -0.1, 0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9,
        1.0,
        9999)
    bins_polarity = len(bins_number_polarity) * [0]

    bins_number_chars = list(range(80))
    bins_number_chars = [i * 10 for i in bins_number_chars]
    bins_chars = len(bins_number_chars) * [0]

    bins_number_words = list(range(50))
    bins_number_words = [i * 2 for i in bins_number_words]
    bins_words = len(bins_number_words) * [0]

    for info in tweets_info:
        append_to_bin(info[2], bins_number_chars, bins_chars)
        append_to_bin(info[3], bins_number_words, bins_words)
        append_to_bin(info[4], bins_number_polarity, bins_polarity)
        append_to_bin(info[5], bins_number_subjectivity, bins_subject)

    file_name = 'bins-output-trolls-2807.txt'
    with open(file_name, 'a') as the_file:
        the_file.write("\n".join(str(item) for item in bins_chars))
        the_file.write("\n------------------\n")
        the_file.write("\n".join(str(item) for item in bins_words))
        the_file.write("\n------------------\n")
        the_file.write("\n".join(str(item) for item in bins_polarity))
        the_file.write("\n------------------\n")
        the_file.write("\n".join(str(item) for item in bins_subject))


def count_ratio_follower_followee(tweets_info):
    multiplier = 1
    tab = (1, 2, 3, 4, 5, 6, 7, 8, 9)
    bins_ratios = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]

    while bins_ratios[len(bins_ratios) - 1] < 29000000:
        bins_ratios.extend([i * multiplier for i in tab])
        multiplier *= 10

    bins_polarity = len(bins_ratios) * [0]

    bins_avg_follower = []
    for i in range(len(bins_ratios)):
        bins_avg_follower.append([])

    for info in tweets_info:
        index = append_to_bin(info[0], bins_ratios, bins_polarity)
        bins_avg_follower[index].append(info[1])

    # 2dim ratio - followeers
    # avgs_ = []
    # for values in bins_avg_follower:
    #     if len(values) > 0:
    #         avgs_.append(mean(values))
    #     else:
    #         avgs_.append(-1)

    file_name = 'normal-ratio-1106.txt'
    with open(file_name, 'a') as the_file:
        the_file.write("\n".join(str(item) for item in bins_polarity))


def count_retweeted_user_ratio_folloers_followees(tweets_info):
    multiplier = 1
    tab = (1, 2, 3, 4, 5, 6, 7, 8, 9)
    bins_ratios = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]

    while bins_ratios[len(bins_ratios) - 1] < 29000000:
        bins_ratios.extend([i * multiplier for i in tab])
        multiplier *= 10

    bins_counters = len(bins_ratios) * [0]
    bins_avg_ratio = len(bins_ratios) * [[]]

    for info in tweets_info:
        ratio = calculate_ratio_follower_following(info[0], info[1])
        index = append_to_bin(ratio, bins_ratios, bins_counters)
        bins_avg_ratio[index].append(info[1])

    avgs_ = []
    for values in bins_avg_ratio:
        if len(values) > 0:
            avgs_.append(mean(values))
        else:
            avgs_.append(-1)

    file_name = 'retweeted-users-follofollowe-HARVARD1106.txt'
    with open(file_name, 'a') as the_file:
        the_file.write("\n".join(str(item) for item in bins_counters))


def count_tweeting_frequency(tweets_info):
    multiplier = 1
    tab = (1, 2, 3, 4, 5, 6, 7, 8, 9)
    bins_ratios = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]

    while bins_ratios[len(bins_ratios) - 1] < 20000:
        bins_ratios.extend([i * multiplier for i in tab])
        multiplier *= 10

    bins_polarity = len(bins_ratios) * [0]

    for info in tweets_info:
        index = append_to_bin(info[2], bins_ratios, bins_polarity)

    file_name = 'troll-normal-freq-more-bins.txt'
    with open(file_name, 'a') as the_file:
        the_file.write("\n".join(str(item) for item in bins_polarity))


def count_avgs(tweets_info):
    count = len(tweets_info)
    avg_chars, avg_words, avg_polarity, avg_subjectivity = 0, 0, 0, 0
    for info in tweets_info:
        avg_chars = avg_chars + info[2] / count
        avg_words = avg_words + info[3] / count
        avg_polarity = avg_polarity + info[4] / count
        avg_subjectivity = avg_subjectivity + info[5] / count

    print("\nAVG:")
    print(avg_chars)
    print(avg_words)
    print(avg_polarity)
    print(avg_subjectivity)


def load_text_analysis_data_from_file():
    tweets_info = set()
    f = open('text-out-troll-users-2107aa.txt', "r")

    for line in f:
        splitted = line.split(",")

        id = splitted[0].strip()
        tweet_id = splitted[1].strip()
        chars_number = int(splitted[2].strip())
        words_number = int(splitted[3].strip())
        polarity = float(splitted[4].strip())
        subjectivity = float(splitted[5].strip())

        tweets_info.add((id, tweet_id, chars_number, words_number, polarity, subjectivity))

    return tweets_info


def analyse_from_file():
    tweets_info = load_text_analysis_data_from_file()

    print("END loading data. Now calculate results.")
    count_avgs(tweets_info)
    count_bins(tweets_info)


def prepare_data_for_2dim_analysis():
    connection = psycopg2.connect("dbname=twitter-us-election user=postgres password=1234")
    cursor = connection.cursor()
    # query = 'SELECT id, tweet_id, tweet_text FROM tweets WHERE tweet_language = \'en\''
    query = 'SELECT id, id_str, text from tweets_n where lang = \'en\''
    cursor.execute(query)

    blobber = Blobber(analyzer=NaiveBayesAnalyzer())
    tweets_info = set()
    for row in cursor:
        id_db = row[0]
        tweet_id = row[1]
        chars_number, words_number, polarity, subjectivity, tag = analyse_tweet_text(row[2], blobber)

        tweets_info.add((id_db, tweet_id, chars_number, words_number, polarity, subjectivity, tag))

    return tweets_info


def two_dimensional_analysis():
    w, h = 11, 21
    result = [[0 for x in range(w)] for y in range(h)]

    tweets_data = prepare_data_for_2dim_analysis()  # load_data_from_file()

    bins_number_subjectivity = (0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 9999)
    bins_subject = len(bins_number_subjectivity) * [0]

    bins_number_polarity = (
        -1.0, -0.9, -0.8, -0.7, -0.6, -0.5, -0.4, -0.3, -0.2, -0.1, 0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9,
        1.0, 9999)
    bins_polarity = len(bins_number_polarity) * [0]

    for tweet in tweets_data:
        id = tweet[0]
        polarity = tweet[4]
        subjectivity = tweet[5]

        polarity_bin = append_to_bin(polarity, bins_number_polarity, bins_polarity)
        subjectivity_bin = append_to_bin(subjectivity, bins_number_subjectivity, bins_subject)

        result[polarity_bin][subjectivity_bin] += 1

    file_name = 'analysis-out-normal-2dimensional-FIXED.txt'
    with open(file_name, 'a') as the_file:
        for list in result:
            for counter in list:
                the_file.write(str(counter) + ", ")
            the_file.write("\n")

    file_name = 'HARVARD-polarity-FIXED.txt'
    with open(file_name, 'a') as the_file:
        the_file.write("\n".join(str(item) for item in bins_polarity))
        the_file.write("\n------------------\n")


def analyse_text():
    switch_to_trolls = False
    if switch_to_trolls:
        query = 'SELECT id, tweet_id, tweet_text FROM tweets WHERE tweet_language = \'en\''
    else:
        query = 'SELECT id, id_str, text from tweets_n where lang = \'en\''    # and user_verified is true

    connection = psycopg2.connect("dbname=twitter-us-election user=postgres password=1234")
    cursor = connection.cursor()
    cursor.execute(query)

    blobber = Blobber(analyzer=NaiveBayesAnalyzer())
    tweets_info = set()
    for row in cursor:
        id_db = row[0]
        tweet_id = row[1]
        chars_number, words_number, polarity, subjectivity, tag = analyse_tweet_text(row[2], blobber)

        tweets_info.add((id_db, tweet_id, chars_number, words_number, polarity, subjectivity, tag))

    connection.close()

    # file_name = 'text-out-troll-users-2807aa.txt'
    # with open(file_name, 'a') as the_file:
    #     for info in tweets_info:
    #         the_file.write(str(info[0]) + ", " + info[1] + ", " + str(info[2]) + ", " + str(info[3]) + ", " + str(
    #             info[4]) + ", " + str(info[5]) + "\n")

    print("data in output file")
    count_avgs(tweets_info)
    count_bins(tweets_info)


def analyse_urls():
    switch_to_trolls = True
    if switch_to_trolls:
        query = 'SELECT urls FROM tweets WHERE urls != \'\' AND urls != \'[]\' AND tweet_language = \'en\''
    else:
        query = 'SELECT urls FROM tweets_n WHERE urls != \'\' AND lang = \'en\''

    connection = psycopg2.connect("dbname=twitter-us-election user=postgres password=1234")
    cursor = connection.cursor()
    cursor.execute(query)

    portals_dict = dict()

    for row in cursor:
        urls = row[0]

        portals_from_urls = parse_urls_from_db(urls)

        for portal in portals_from_urls:
            if portal in portals_dict:
                portals_dict[portal] += 1
            else:
                portals_dict[portal] = 1

    print("Counting ended. Writing to file.")

    portals_dict = sorted(portals_dict.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)

    file_name = 'analysis-urls-ira-eng-1306.txt'
    with open(file_name, 'a', encoding="utf-8") as the_file:
        for elem in portals_dict:
            the_file.write(str(elem[0]) + ", " + str(elem[1]) + "\n")


def analyse_ratios_follower_followees():
    connection = psycopg2.connect("dbname=twitter-us-election user=postgres password=1234")
    cursor = connection.cursor()
    switch_to_trolls = False

    if switch_to_trolls:
        query = 'SELECT CAST(follower_count AS float) / CAST(following_count + 1 AS float) as Ratio, follower_count, user_id FROM tweets GROUP BY user_id, follower_count, following_count;'
    else:
        query = 'SELECT (MAX(ratio)) as Ratio_, user_id_str FROM (SELECT user_id_str, CAST(user_followers_count AS float) / CAST(user_friends_count + 1 AS float) as Ratio, MAX(user_followers_count) FROM tweets_n GROUP BY user_id_str, user_description, user_followers_count, user_friends_count) as tt GROUP BY user_id_str'

    cursor.execute(query)

    data = []

    for row in cursor:
        data.append(row)

    count_ratio_follower_followee(data)


def analyse_tweeting_frequency():
    connection = psycopg2.connect("dbname=twitter-us-election user=postgres password=1234")
    cursor = connection.cursor()
    query = 'SELECT tweets_number, days_active, days_active::float8 / tweets_number::float8 as tweeting_frequency, account_creation_date, last_activity_date FROM (SELECT user_created_at as account_creation_date, max(created_at) as last_activity_date, count(*) as tweets_number, date(max(created_at)) - date(user_created_at) as days_active FROM tweets_n GROUP BY user_id_str, user_created_at) as i order by tweeting_frequency;'
    # query = 'SELECT tweets_number, days_active, days_active::float8 / tweets_number::float8 as tweeting_frequency, account_creation_date, last_activity_date FROM (SELECT user_id, account_creation_date, date(max(tweet_time)) as last_activity_date, count(*) as tweets_number, date(max(tweet_time)) - account_creation_date as days_active FROM tweets GROUP BY user_id, account_creation_date) as i order by tweeting_frequency'
    cursor.execute(query)

    data = []

    for row in cursor:
        data.append(row)

    count_tweeting_frequency(data)


def analyse_twitter_clients():
    switch_to_trolls = False
    if switch_to_trolls:
        query = 'SELECT tweet_client_name FROM tweets WHERE tweet_language = \'en\''
    else:
        query = 'SELECT source FROM tweets_n WHERE lang = \'en\''

    connection = psycopg2.connect("dbname=twitter-us-election user=postgres password=1234")
    cursor = connection.cursor()
    cursor.execute(query)

    client_categories_counters = {'official-mobile': 0, 'official-pc': 0, 'popular-unofficial': 0, 'unofficial': 0}

    for row in cursor:
        tweet_client_name = row[0]
        tweet_client_category = assign_category_to_twitter_client(tweet_client_name)
        client_categories_counters[tweet_client_category] += 1

    file_name = 'analysis-categories-client-harvard-en-1306.txt'
    with open(file_name, 'a') as the_file:
        for key, value in client_categories_counters.items():
            the_file.write(str(key) + ", " + str(value) + "\n")


def analyse_message_similarity_tensorflow():
    switch_to_trolls = False
    if switch_to_trolls:
        query = 'SELECT user_id, tweet_id, tweet_text FROM tweets WHERE tweet_language = \'en\''
    else:
        query = 'SELECT user_id_str, id_str, text FROM tweets_n WHERE lang = \'en\''

    connection = psycopg2.connect("dbname=twitter-us-election user=postgres password=1234")
    cursor = connection.cursor()
    cursor.execute(query)

    avg_similarities_list, similar_numbers_list = perform_message_similarity_analysis_results_in_lists(cursor, 0.7)
    # [i for i in avg_similarities_list if i < 0]
    # sum(elem < 0 for elem in avg_similarities_list)

    bins_number_avg_similarity = (0.0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1.0, 9999)
    bins_avg_similarity = len(bins_number_avg_similarity) * [0]

    bins_similar_number = 6000 * [0]

    for avg_similarity, similar_number in zip(avg_similarities_list, similar_numbers_list):
        append_to_bin(avg_similarity, bins_number_avg_similarity, bins_avg_similarity)
        bins_similar_number[similar_number] += 1

    file_name = 'bins-output-ira-similarity-analysisV4-07.txt'
    with open(file_name, 'a') as the_file:
        the_file.write("\n".join(str(item) for item in bins_avg_similarity))
        the_file.write("\n------------------\n")
        the_file.write("\n------------------\n")
        the_file.write("\n------------------\n")
        the_file.write("\n".join(str(item) for item in bins_similar_number))


def analyse_retweeted_user_ratio_follower_followees():
    switch_to_trolls = False
    if switch_to_trolls:
        query = 'SELECT r_user_followers_count, r_user_friends_count FROM tweets WHERE r_user_followers_count is not null'
    else:
        query = 'SELECT r_user_followers_count, r_user_friends_count FROM tweets_n WHERE r_user_followers_count is not null'

    connection = psycopg2.connect("dbname=twitter-us-election user=postgres password=1234")
    cursor = connection.cursor()
    cursor.execute(query)

    count_retweeted_user_ratio_folloers_followees(cursor)


def analyse_user_favorite_client_category():
    switch_to_trolls = False
    if switch_to_trolls:
        # query = 'SELECT a.user_id, a.tweet_client_name, a.count FROM (select user_id, tweet_client_name, count(*) as count from tweets group by user_id, tweet_client_name) as a INNER JOIN (SELECT user_id, MAX(count) count FROM (select user_id, count(*) as count from tweets group by user_id, tweet_client_name) as aa GROUP BY user_id) b ON a.user_id = b.user_id AND a.count = b.count'
        query = 'SELECT a.user_id, a.tweet_client_name, a.count FROM (select user_id, tweet_client_name, count(*) as count from tweets where tweet_language =\'en\' group by user_id, tweet_client_name) as a INNER JOIN (SELECT user_id, MAX(count) count FROM (select user_id, count(*) as count from tweets where tweet_language =\'en\' group by user_id, tweet_client_name) as aa GROUP BY user_id) b ON a.user_id = b.user_id AND a.count = b.count'
    else:
        query = 'SELECT a.user_id_str, a.source, a.count FROM (select user_id_str, source, count(*) as count from tweets_n where lang = \'en\' group by user_id_str, source) as a INNER JOIN (SELECT user_id_str, MAX(count) count FROM (select user_id_str, count(*) as count from tweets_n where lang = \'en\' group by user_id_str, source) as aa GROUP BY user_id_str) b ON a.user_id_str = b.user_id_str AND a.count = b.count'

    connection = psycopg2.connect("dbname=twitter-us-election user=postgres password=1234")
    cursor = connection.cursor()
    cursor.execute(query)

    map_user_id_to_result = get_user_favorite_client_category_and_clients(cursor)

    client_categories_counters = {'official-mobile': 0, 'official-pc': 0, 'popular-unofficial': 0,
                                  'unofficial': 0, 'multiple-only-official': 0,
                                  'multiple-only-unofficial': 0, 'multiple-both-categories': 0}

    for user_id, result_tuple in map_user_id_to_result.items():
        category = result_tuple[1]
        client_categories_counters[category] += 1

    file_name = 'analysis-user-favorite-client-category-harvard-ENG-1106.txt'
    with open(file_name, 'a') as the_file:
        for key, value in client_categories_counters.items():
            the_file.write(str(key) + ", " + str(value) + "\n")


import matplotlib.pyplot as plt
from matplotlib import rcParams


def append_to_bins_follower_following(tweets_info):
    # bins_labels_followers = get_bins_x10(7)
    bins_labels_followers = list(range(0, 257639))      # 257639 79546533
    bins_followers = [0] * len(bins_labels_followers)

    # bins_labels_following = get_bins_x10(6)
    bins_labels_following = list(range(0, 74665))       # 74665 1183263
    bins_following = [0] * len(bins_labels_following)

    for info in tweets_info:
        # append_to_bin(info[1], bins_labels_followers, bins_followers)
        # append_to_bin(info[2], bins_labels_following, bins_following)
        bins_followers[info[1]] += 1
        bins_following[info[2]] += 1

    rcParams['figure.figsize'] = 15, 10
    plt.title('Liczba użytkowników z określoną liczbą obserwujących')
    plt.xlabel('Liczba obserwujących')
    plt.ylabel('Liczba użytkowników')
    plt.plot(bins_labels_followers, bins_followers)
    plt.xscale('symlog')

    plt.savefig("followers-trolls.png")
    plt.show()

    # second diagram
    rcParams['figure.figsize'] = 15, 10
    plt.title('Liczba użytkowników obserwująca określoną liczbę użytkowników')
    plt.xlabel('Liczba obserwowanych')
    plt.ylabel('Liczba użytkowników')
    plt.plot(bins_labels_following, bins_following)
    plt.xscale('symlog')

    plt.savefig("friends-trolls.png")
    plt.show()

    # file_name = 'bins-follower-following-harvard-allbbb.txt'
    # with open(file_name, 'a') as the_file:
    #     the_file.write("\n".join(str(item) for item in bins_followers))
    #     the_file.write("\n------------------\n")
    #     the_file.write("\n------------------\n")
    #     the_file.write("\n------------------\n")
    #     the_file.write("\n".join(str(item) for item in bins_following))


def followeer_followee_to_bins():
    switch_to_trolls = True
    if switch_to_trolls:
        query = 'select user_id, max(follower_count) as follower, max(following_count) as following from tweets group by user_id'
    else:
        query = 'select user_id_str, max(user_followers_count) as follower, max(user_friends_count) as following from tweets_n group by user_id_str;'

    connection = psycopg2.connect("dbname=twitter-us-election user=postgres password=1234")
    cursor = connection.cursor()
    cursor.execute(query)

    append_to_bins_follower_following(cursor)


def apend_to_bins_likes(tweets_info):
    bins_labels_likes = get_bins_x10(5)
    bins_likes = [0] * len(bins_labels_likes)

    for info in tweets_info:
        append_to_bin(info[1], bins_labels_likes, bins_likes)

    file_name = 'bins-likes-harvard.txt'
    with open(file_name, 'a') as the_file:
        the_file.write("\n".join(str(item) for item in bins_likes))


def tweets_likes_to_bins():
    switch_to_trolls = True
    if switch_to_trolls:
        query = 'select tweet_id, like_count from tweets;'
    else:
        query = 'select id_str, favorite_count from tweets_n;'

    connection = psycopg2.connect("dbname=twitter-us-election user=postgres password=1234")
    cursor = connection.cursor()
    cursor.execute(query)

    apend_to_bins_likes(cursor)


def apend_to_bins_emotions(emotions_analysis_results, out_file_name):
    bins_emotions_in_top_5 = [0] * 64
    bins_top1_emotion = [0] * 64

    for result in emotions_analysis_results:
        bins_top1_emotion[result[2]] += 1
        for i in range(0, 5):
            bins_emotions_in_top_5[result[i + 2]] += 1

    with open(out_file_name, 'a') as the_file:
        the_file.write("\nEmotions occurences in top five.\n")
        the_file.write("\n".join(str(item) for item in bins_emotions_in_top_5))
        the_file.write("\n--------------------------------\n")
        the_file.write("\nEmotions with the most share - top 1.\n")
        the_file.write("\n".join(str(item) for item in bins_top1_emotion))


def analyse_tweets_emotions(input_file, out_file_name):
    emotions_analysis_results = []
    f = open(input_file, "r")

    for line in f:
        splitted = line.split(",")

        tweet_id = splitted[0].strip()
        sum_of_5 = float(splitted[1].strip())
        emotion_nr_1 = int(splitted[2].strip())
        emotion_nr_2 = int(splitted[3].strip())
        emotion_nr_3 = int(splitted[4].strip())
        emotion_nr_4 = int(splitted[5].strip())
        emotion_nr_5 = int(splitted[6].strip())
        emotion_nr_1_part = float(splitted[7].strip())
        emotion_nr_2_part = float(splitted[8].strip())
        emotion_nr_3_part = float(splitted[9].strip())
        emotion_nr_4_part = float(splitted[10].strip())
        emotion_nr_5_part = float(splitted[11].strip())

        emotions_analysis_results.append((tweet_id, sum_of_5, emotion_nr_1, emotion_nr_2, emotion_nr_3, emotion_nr_4, emotion_nr_5,
                                          emotion_nr_1_part, emotion_nr_2_part, emotion_nr_3_part, emotion_nr_4_part, emotion_nr_5_part))

    apend_to_bins_emotions(emotions_analysis_results, out_file_name)


def run_emotions_analysis_and_save_results_to_file():
    switch_to_trolls = False
    if switch_to_trolls:
        query = 'SELECT tweet_id, tweet_text FROM tweets WHERE tweet_language = \'en\''
    else:
        query = 'SELECT id_str, text from tweets_n where lang = \'en\''  # and user_verified is true

    connection = psycopg2.connect("dbname=twitter-us-election user=postgres password=1234")
    cursor = connection.cursor()
    cursor.execute(query)

    sentence_tokenizer, model = init_tokenizer_emotions(max_len=70)

    file_name = 'teteteds4326.txt'
    with open(file_name, 'a') as the_file:
        tweets_id_text = []
        for row in cursor:
            tweet_id = row[0]
            preprocessed_tweet_text = preprocess_tweet_text_advanced(row[1])

            if preprocessed_tweet_text != '':
                tweets_id_text.append((tweet_id, preprocessed_tweet_text))

            if len(tweets_id_text) >= 250000:
                results = perform_text_emotions_analysis(tweets_id_text, sentence_tokenizer, model)
                for result in results:
                    the_file.write(",".join(str(value) for value in result) + "\n")
                tweets_id_text = []

        if len(tweets_id_text) > 0:
            results = perform_text_emotions_analysis(tweets_id_text, sentence_tokenizer, model)
            for result in results:
                the_file.write(",".join(str(value) for value in result) + "\n")


def run_urls_category_analysis(output_file_name, switch_to_trolls=True):
    if switch_to_trolls:
        query = 'SELECT urls FROM tweets WHERE urls != \'\' AND urls != \'[]\' AND tweet_language = \'en\''
    else:
        query = 'SELECT urls FROM tweets_n WHERE urls != \'\' AND lang = \'en\''

    connection = psycopg2.connect("dbname=twitter-us-election user=postgres password=1234")
    cursor = connection.cursor()
    cursor.execute(query)

    portal_categories_counters = {'twitter': 0, 'shortener': 0, 'news': 0, 'social': 0, 'media': 0, 'other': 0, 'multi': 0}

    for row in cursor:
        urls = row[0]
        portals_from_urls = parse_urls_from_db(urls)
        portal_category = check_portals_category(portals_from_urls)
        portal_categories_counters[portal_category] += 1

    with open(output_file_name, 'a') as the_file:
        for key, value in portal_categories_counters.items():
            the_file.write(str(key) + ", " + str(value) + "\n")


if __name__ == '__main__':

    # tweet_text = '@Trump'
    # blobber = Blobber(analyzer=NaiveBayesAnalyzer())
    # chars_number, words_number, polarity, subjectivity, tag = analyse_tweet_text(tweet_text, blobber)

    # analyse_ratios_follower_followees()
    # analyse_retweeted_user_ratio_follower_followees()
    # analyse_user_favorite_client_category()
    # analyse_text()
    # analyse_message_similarity_tensorflow()
    # analyse_twitter_clients()
    # analyse_urls()
    # followeer_followee_to_bins()
    tweets_likes_to_bins()

    # analyse_tweets_emotions(input_file="emotions_out_troll.txt", out_file_name='trolls_emotions_bins.txt')
    # run_emotions_analysis_and_save_results_to_file()


    # tego 2 raz nie odpalam, przynajmniej narazie
    # two_dimensional_analysis()

    # analyse_from_file()

    # run_urls_category_analysis("output-urls-categories-harv.txt", switch_to_trolls=False)

    pass
