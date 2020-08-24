import time


def get_usersids_to_filter_out(clustering_data_file, clusters_numbers_to_remove):
    f = open(clustering_data_file, "r")

    users_to_remove = set()

    for line in f:
        splitted = line.split(",")

        tweet_id = splitted[0].strip()
        cluster_number = int(splitted[1].strip())
        user_id = splitted[2].strip()

        if cluster_number in clusters_numbers_to_remove:
            users_to_remove.add(user_id)

    f.close()
    return users_to_remove


def filter_elements_from_given_clusters(tweets_data_file, clustering_data_file, clusters_numbers_to_remove):

    timestr = time.strftime("%Y%m%d-%H%M%S")
    data_after_filter = 'data_after_filter_' + timestr + '.txt'
    removed_data = 'filtered_out_' + timestr + '.txt'

    users_to_remove = get_usersids_to_filter_out(clustering_data_file, clusters_numbers_to_remove)

    with open(tweets_data_file, 'r', encoding="utf-8") as analyses_data_file_, \
            open(data_after_filter, 'w', encoding="utf-8") as data_after_filter_, \
            open(removed_data, 'w', encoding="utf-8") as removed_data_:

        for line in analyses_data_file_:
            splitted = line.split(",")
            user_id = splitted[0].strip()
            if user_id in users_to_remove:
                removed_data_.write(line)
            else:
                data_after_filter_.write(line)


def get_only_retweets_lines(tweets_data_file, output_file):
    with open(tweets_data_file, 'r', encoding="utf-8") as analyses_data_file_, \
            open(output_file, 'w', encoding="utf-8") as output_file_:

        for line in analyses_data_file_:
            splitted = line.split(",")
            retweeted_user_ratio_follower_following = float(splitted[16].strip())
            if retweeted_user_ratio_follower_following > -0.1:
                output_file_.write(line)


if __name__ == '__main__':
    # filter_elements_from_given_clusters(tweets_data_file="final-concat-normal-2807.txt",
    #                                     clustering_data_file="clusters-4cechy.txt",
    #                                     clusters_numbers_to_remove=[1, 2, 4])

    # get_only_retweets_lines(tweets_data_file="final-concat-troll-2807.txt",
    #                         output_file="filtered-trolls-only-retweet.txt")

    get_only_retweets_lines(tweets_data_file="data_after_filter_20200731-230455.txt",
                            output_file="filtered-normal-only-retweet.txt")

    print("DONE")
