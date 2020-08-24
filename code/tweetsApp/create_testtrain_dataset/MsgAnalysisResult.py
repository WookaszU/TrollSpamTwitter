class AnalysisResult:

    def __init__(self, user_id, tweet_id, label):
        self.user_id = user_id
        self.tweet_id = tweet_id
        self.label = label
        # metrics
        self.chars_number = None
        self.words_number = None
        self.polarity = None
        self.subjectivity = None
        self.tag = None
        self.max_serie_size = None
        self.portals_in_tweet = None
        self.urls_number = None
        self.url_portal_category = 'none'
        self.tweeting_frequency = None
        self.hashtags_count = None
        self.user_mentions_count = None
        self.favorite_count = None
        self.tweet_client_name = None
        self.tweet_client_category = None
        self.follower_count = None
        self.following_count = None
        self.ratio_follower_following = None
        self.avg_similarity = None
        self.num_of_similar_messages = None
        self.favorite_client_name = None
        self.favorite_client_category = None

        self.retweeted_user_ratio_follower_following = None
        self.retweet_maximal_clique_in_size = 1
        self.retweet_maximal_cliques_in_number = 0
        self.top_n_series_avg = None
        self.max_tweets_number_in_time_window = None

    def set_chars_number(self, chars_number):
        self.chars_number = chars_number

    def set_polarity(self, polarity):
        self.polarity = polarity

    def set_words_number(self, words_number):
        self.words_number = words_number

    def set_subjectivity(self, subjectivity):
        self.subjectivity = subjectivity

    def set_tag(self, tag):
        self.tag = tag

    def set_tweet_series_analysis_results(self, max_serie_size, top_n_series_avg):
        self.max_serie_size = max_serie_size
        self.top_n_series_avg = top_n_series_avg

    def set_max_tweets_number_in_time_window(self, max_tweets_number_in_time_window):
        self.max_tweets_number_in_time_window = max_tweets_number_in_time_window

    def set_tweeting_frequency(self, tweeting_frequency):
        self.tweeting_frequency = tweeting_frequency

    def set_favorite_count(self, favorite_count):
        self.favorite_count = favorite_count

    def set_tweet_client_name(self, tweet_client_name):
        self.tweet_client_name = tweet_client_name

    def set_tweet_client_name_and_category(self, tweet_client_name, tweet_client_category):
        self.tweet_client_name = tweet_client_name
        self.tweet_client_category = tweet_client_category

    def set_text_analysis_results(self, chars_number, words_number, polarity, subjectivity, tag,
                                  hashtags_count, user_mentions_count):
        self.chars_number = chars_number
        self.words_number = words_number
        self.polarity = polarity
        self.subjectivity = subjectivity
        self.tag = tag
        self.hashtags_count = hashtags_count
        self.user_mentions_count = user_mentions_count

    def set_url_analysis_result(self, portals_in_tweet, url_portal_category):
        self.portals_in_tweet = portals_in_tweet
        self.urls_number = len(portals_in_tweet)
        self.url_portal_category = url_portal_category

    def set_user_data(self, follower_count, following_count, ratio_follower_following):
        self.follower_count = follower_count
        self.following_count = following_count
        self.ratio_follower_following = ratio_follower_following

    def set_similarity_analysis_result(self, avg_similarity, num_of_similar_messages):
        self.avg_similarity = avg_similarity
        self.num_of_similar_messages = num_of_similar_messages

    def set_favorite_client_analysis_result(self, favorite_client_name, favorite_client_category):
        self.favorite_client_name = favorite_client_name
        self.favorite_client_category = favorite_client_category

    def set_graph_analysis_result(self, maximal_clique_in_size, maximal_cliques_in_number):
        self.retweet_maximal_clique_in_size = maximal_clique_in_size
        self.retweet_maximal_cliques_in_number = maximal_cliques_in_number

    def set_retweeted_user_ratio(self, retweeted_user_ratio_follower_following):
        self.retweeted_user_ratio_follower_following = retweeted_user_ratio_follower_following

    def convert_to_weka_data_row_format(self):
        return ','.join(
            (str(self.user_id),
             str(self.tweet_id),
             str(self.chars_number),
             str(self.words_number),
             str(self.polarity),
             str(self.subjectivity),
             str(self.tag),  # @ATTRIBUTE tag {pos,neg}
             str(self.max_serie_size),
             # str('[' + ', '.join(self.portals_in_tweet) + ']'),
             str(self.urls_number),
             # str(self.tweeting_frequency),
             str(self.hashtags_count),
             str(self.user_mentions_count),
             str(self.favorite_count),
             # str(self.tweet_client_name.replace(" ", "")),
             str(self.tweet_client_category),
             str(self.follower_count),
             str(self.following_count),
             str(self.ratio_follower_following),

             str(self.retweeted_user_ratio_follower_following),
             str(self.retweet_maximal_clique_in_size),
             str(self.retweet_maximal_cliques_in_number),
             str(self.top_n_series_avg),
             str(self.max_tweets_number_in_time_window),

             str(self.avg_similarity),
             str(self.num_of_similar_messages),
             # str(self.favorite_client_name),
             str(self.favorite_client_category),
             str(self.url_portal_category),

             str(self.label))
        )
