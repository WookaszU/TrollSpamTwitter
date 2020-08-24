from sklearn import datasets
from sklearn.cluster import KMeans
import pandas as pd
from sklearn import preprocessing
import numpy as np
import time


def load_data_from_file(file_name):
    tweets_list = []
    f = open(file_name, "r")

    # user_id_found_200 = set()
    # user_id_found_500 = set()

    i = 0
    for line in f:

        # i += 1
        # if i > 10:
        #     break

        splitted = line.split(",")

        # user_id = splitted[0].strip()
        tweet_id = splitted[1].strip()
        chars_number = int(splitted[2].strip())
        words_number = int(splitted[3].strip())
        polarity = float(splitted[4].strip())
        subjectivity = float(splitted[5].strip())
        # tag = splitted[6].strip()
        max_serie_size = int(splitted[7].strip())
        urls_number = int(splitted[8].strip())
        hashtags_count = int(splitted[9].strip())
        user_mentions_count = int(splitted[10].strip())
        favorite_count = int(splitted[11].strip())
        tweet_client_category = splitted[12].strip()
        follower_count = int(splitted[13].strip())
        following_count = int(splitted[14].strip())
        ratio_follower_following = float(splitted[15].strip())
        retweeted_user_ratio_follower_following = float(splitted[16].strip())
        retweet_maximal_clique_in_size = int(splitted[17].strip())
        retweet_maximal_cliques_in_number = int(splitted[18].strip())
        top_n_series_avg = float(splitted[19].strip())
        max_tweets_number_in_time_window = int(splitted[20].strip())
        avg_similarity = float(splitted[21].strip())
        num_of_similar_messages = int(splitted[22].strip())
        favorite_client_category = splitted[23].strip()
        url_portal_category = splitted[24].strip()

        # sum_of_5 = float(splitted[25].strip())
        emotion_nr_1 = int(splitted[26].strip())
        # emotion_nr_2 = int(splitted[27].strip())
        # emotion_nr_3 = int(splitted[28].strip())
        # emotion_nr_4 = int(splitted[29].strip())
        # emotion_nr_5 = int(splitted[30].strip())
        # emotion_nr_1_part = float(splitted[31].strip())
        # emotion_nr_2_part = float(splitted[32].strip())
        # emotion_nr_3_part = float(splitted[33].strip())
        # emotion_nr_4_part = float(splitted[34].strip())
        # emotion_nr_5_part = float(splitted[35].strip())

        # label = splitted[36].strip()

        # if num_of_similar_messages > 200:
        #     if num_of_similar_messages > 500:
        #         user_id_found_500.add(user_id)
        #     else:
        #         user_id_found_200.add(user_id)

        tweets_list.append((
            # user_id,
            tweet_id,
            chars_number,
            words_number,
            polarity,
            subjectivity,
            max_serie_size,
            urls_number,
            hashtags_count,
            user_mentions_count,
            favorite_count,
            tweet_client_category,
            follower_count,
            following_count,
            ratio_follower_following,
            retweeted_user_ratio_follower_following,
            retweet_maximal_clique_in_size,
            retweet_maximal_cliques_in_number,
            top_n_series_avg,
            max_tweets_number_in_time_window,
            avg_similarity,
            num_of_similar_messages,
            favorite_client_category,
            url_portal_category,
            # sum_of_5,
            emotion_nr_1,
            # emotion_nr_2,
            # emotion_nr_3,
            # emotion_nr_4,
            # emotion_nr_5,
            # emotion_nr_1_part,
            # emotion_nr_2_part,
            # emotion_nr_3_part,
            # emotion_nr_4_part,
            # emotion_nr_5_part,
            #     # label
        ))

    in_dataframe = pd.DataFrame(tweets_list)

    del tweets_list[:]
    del tweets_list

    return in_dataframe


def preprocess_data(tweets):
    tweets_ids = tweets[tweets.columns[0]]
    tweets.drop(tweets.columns[0], axis=1, inplace=True)

    le = preprocessing.LabelEncoder()
    tweets[10] = le.fit_transform(tweets[10])
    tweets[21] = le.fit_transform(tweets[21])
    tweets[22] = le.fit_transform(tweets[22])

    return tweets_ids, tweets


def preprocess_data_with_user_id(tweets):
    users_ids = tweets[tweets.columns[0]]
    tweets_ids = tweets[tweets.columns[1]]
    tweets.drop(tweets.columns[0], axis=1, inplace=True)
    tweets.drop(tweets.columns[0], axis=1, inplace=True)

    le = preprocessing.LabelEncoder()
    tweets[11] = le.fit_transform(tweets[11])
    tweets[22] = le.fit_transform(tweets[22])
    tweets[23] = le.fit_transform(tweets[23])

    return users_ids, tweets_ids, tweets


def cluster_and_save_results(tweets_ids, tweets, clusters_number, users_ids=None):
    kmeans = KMeans(n_clusters=clusters_number, random_state=0).fit(tweets)
    res = kmeans.labels_
    buckets_counts = [0] * clusters_number
    for bucket_number in res:
        buckets_counts[bucket_number] += 1

    timestr = time.strftime("%Y%m%d-%H%M%S")
    clustering_details_file = 'z-clusters-centers' + timestr + '.txt'
    clustering_results_file = 'z-tweets_id_clusters' + timestr + '.txt'

    np.savetxt(clustering_details_file, kmeans.cluster_centers_, fmt='%f')

    dataset_elements = len(tweets)
    with open(clustering_details_file, 'a', encoding="utf-8") as the_file:
        the_file.write("\nClusters percentage distribution:\n")
        for id_, value in enumerate(buckets_counts):
            the_file.write(str(id_) + ": " + str(round((value / dataset_elements) * 100, 2)) + "\n")

    if users_ids is not None:
        tweets_ids_with_clusters = np.vstack((tweets_ids, res, users_ids)).T
        np.savetxt(clustering_results_file, tweets_ids_with_clusters, fmt='%s, %d, %s')
    else:
        tweets_ids_with_clusters = np.vstack((tweets_ids, res)).T
        np.savetxt(clustering_results_file, tweets_ids_with_clusters, fmt='%s, %d')


if __name__ == '__main__':
    # tweets = load_data_from_file(file_name='data_after_filter_20200731-230455.txt')
    tweets = load_data_from_file(file_name='filtered-normal-only-retweet.txt')
    tweets_ids, tweets = preprocess_data(tweets)
    cluster_and_save_results(tweets_ids, tweets, 4)

    print("DONE")
