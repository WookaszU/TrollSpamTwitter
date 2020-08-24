import random


def get_map_tweetid_to_data(file_name):
    map_tweet_id_to_data = {}
    f = open(file_name, "r")

    for line in f:
        splitted = line.split(",")
        tweet_id = splitted[1].strip()
        map_tweet_id_to_data[tweet_id] = line

    return map_tweet_id_to_data


def load_clusters_data(file_name, number_of_clusters):
    tweets_ids_in_clusters = [[] for i in range(number_of_clusters)]
    f = open(file_name, "r")

    for line in f:
        splitted = line.split(",")

        tweet_id = splitted[0].strip()
        cluster_number = int(splitted[1].strip())

        tweets_ids_in_clusters[cluster_number].append(tweet_id)

    return tweets_ids_in_clusters


if __name__ == '__main__':
    elements_to_choose = 160303
    clusters_number = 4
    # tweets_file = "data_after_filter_20200731-230455.txt"
    # tid_cluster_file = "z-tweets_id_clusters20200801-014510.txt"
    # output_file = "normal-users-595k0108"

    tweets_file = "filtered-normal-only-retweet.txt"
    tid_cluster_file = "z-tweets_id_clusters20200802-032917.txt"
    output_file = "normal-only-retweets0208.txt"

    map_tweet_id_to_data = get_map_tweetid_to_data(tweets_file)
    tweets_ids_clusters = load_clusters_data(tid_cluster_file, clusters_number)

    proportions = []
    for i in range(0, clusters_number):
        proportions.append(len(tweets_ids_clusters[i]))

    all_elements_number = sum(proportions)
    number_to_choose_from_each_cluster = [round((elem / all_elements_number) * elements_to_choose) for elem in proportions]

    choosen_tweet_ids = []

    for cluster in range(0, clusters_number):
        choosen_ids = random.sample(tweets_ids_clusters[cluster], number_to_choose_from_each_cluster[cluster])
        choosen_tweet_ids.extend(choosen_ids)

    choosen_tweets = []
    for choosen_tweet_id in choosen_tweet_ids:
        choosen_tweets.append(map_tweet_id_to_data.pop(choosen_tweet_id))

    with open(output_file, 'a', encoding="utf-8") as the_file:
        for tweet_data in choosen_tweets:
            the_file.write(tweet_data)
