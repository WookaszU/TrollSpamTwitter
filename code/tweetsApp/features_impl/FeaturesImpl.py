import math
import re
from collections import deque

import pkg_resources
from numpy import mean
from symspellpy import SymSpell, Verbosity
from textblob import TextBlob, Blobber
from textblob.en.sentiments import NaiveBayesAnalyzer
from tldextract import extract
import tensorflow.compat.v1 as tf
import tensorflow_hub as hub
import numpy as np
import html
import networkx as nx
from torchmoji.sentence_tokenizer import SentenceTokenizer
from torchmoji.model_def import torchmoji_emojis
from torchmoji.global_variables import PRETRAINED_PATH, VOCAB_PATH
import json


def init_symspell():
    # maximum edit distance per dictionary precalculation
    max_edit_distance_dictionary = 1    # bylo tutaj 0
    prefix_length = 100
    # create object
    # sym_spell = SymSpell(max_edit_distance_dictionary, prefix_length)
    sym_spell = SymSpell(max_edit_distance_dictionary, prefix_length)
    # load dictionary
    dictionary_path = pkg_resources.resource_filename(
        "symspellpy", "frequency_dictionary_en_82_765.txt")
    bigram_path = pkg_resources.resource_filename(
        "symspellpy", "frequency_bigramdictionary_en_243_342.txt")
    # term_index is the column of the term and count_index is the
    # column of the term frequency
    if not sym_spell.load_dictionary(dictionary_path, term_index=0,
                                     count_index=1):
        print("Dictionary file not found")
        return
    if not sym_spell.load_bigram_dictionary(dictionary_path, term_index=0,
                                            count_index=2):
        print("Bigram dictionary file not found")
        return

    return sym_spell


sym_spell_ = init_symspell()


# def preproress_tweet_text_base(tweet_text):
#     tweet_text = re.sub(
#         r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)', "",
#         tweet_text, flags=re.MULTILINE)
#     tweet_text = re.sub(r'RT @.*?:', '', tweet_text, flags=re.MULTILINE)
#     tweet_text = tweet_text.strip()
#
#     tweet_text = html.unescape(tweet_text)
#
#     return tweet_text


def preprocess_tweet_text_advanced(tweet_text):
    tweet_text = re.sub(
        r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)', "",
        tweet_text, flags=re.MULTILINE)

    tweet_text = re.sub(r'RT @[^ ]*?:', '', tweet_text, count=1, flags=re.MULTILINE)
    tweet_text = re.sub(r"#", '', tweet_text, flags=re.MULTILINE)     # remove only '#' and '@' characters from hashtag "#|@"
    tweet_text = re.sub(r"@(\w+)", ' ', tweet_text, flags=re.MULTILINE)   # remove user mention
    # tweet_text = re.sub(r"#(\w+)", ' ', tweet_text, flags=re.MULTILINE)   # remove hashtag

    tweet_text = tweet_text.strip()
    tweet_text = html.unescape(tweet_text)
    tweet_text = ' '.join([sym_spell_.lookup(word, Verbosity.CLOSEST, max_edit_distance=1, include_unknown=True)[0].term for word in tweet_text.split()])

    return tweet_text


def basic_blob_analysis(tweet_text):
    blob = TextBlob(tweet_text)
    words_number = len(blob.words)
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity

    return words_number, polarity, subjectivity, None


def stanford_nltk_blob_analysis(tweet_text, blobber):
    blob = blobber(tweet_text)  # TextBlob(tweet_text, analyzer=NaiveBayesAnalyzer())
    words_number = len(blob.words)
    polarity = blob.sentiment.p_pos - blob.sentiment.p_neg
    subjectivity = blob.subjectivity
    tag = blob.sentiment.classification

    return words_number, polarity, subjectivity, tag


def parse_urls_from_db(urls):
    portals_in_tweet_links = []

    if urls[:1] == '[':
        urls = urls[1:-1]

    splitted = urls.split(",")
    if splitted[0] == '':
        return []

    for url in splitted:
        subdomain, domain, suffix = extract(url)
        portal = domain + "." + suffix

        portals_in_tweet_links.append(portal)

    return portals_in_tweet_links


def analyse_tweet_text(tweet_text, blobber):
    tweet_text = preprocess_tweet_text_advanced(tweet_text)  # preproress_tweet_text_base(tweet_text)
    chars_number = len(tweet_text)
    words_number, polarity, subjectivity, tag = stanford_nltk_blob_analysis(tweet_text, blobber)

    return chars_number, words_number, polarity, subjectivity, tag


def update_series_data(top_n_series, max_serie_size, min_in_top_list, number_of_top_series_to_avg, serie_length):
    if serie_length > max_serie_size:
        max_serie_size = serie_length
        top_n_series.pop()
        top_n_series.appendleft(max_serie_size)
    elif serie_length > min_in_top_list:
        top_n_series.pop()

        position = number_of_top_series_to_avg - 1

        while top_n_series[position - 1] < serie_length:
            position -= 1

        top_n_series.insert(position, serie_length)
        min_in_top_list = top_n_series[number_of_top_series_to_avg - 1]

    return max_serie_size, min_in_top_list


#   On input sorted timestamps for each user
#   METRICS: max tweets series with max N minutes time gaps
def analyse_tweets_series_with_time_gaps(users_tweets_timestamps, time_window_minutes, number_of_top_series_to_avg):
    results = []
    time_gap = 60 * time_window_minutes

    for user_id, timestamps in users_tweets_timestamps.items():
        max_serie_size = 0
        top_n_series = deque(number_of_top_series_to_avg * [0], maxlen=number_of_top_series_to_avg)
        min_in_top_list = 0

        timestamps_list_length = len(timestamps)
        if timestamps_list_length < 2:
            results.append([user_id, timestamps_list_length, timestamps_list_length])
        else:
            i = 1
            serie_timestamps = [timestamps[0]]
            while i < len(timestamps):
                current = timestamps[i - 1]
                next_elem = timestamps[i]

                if current + time_gap > next_elem:
                    serie_timestamps.append(next_elem)
                else:
                    serie_length = len(serie_timestamps)
                    max_serie_size, min_in_top_list = update_series_data(top_n_series, max_serie_size, min_in_top_list,
                                                                         number_of_top_series_to_avg, serie_length)
                    serie_timestamps = [next_elem]

                i += 1

            serie_length = len(serie_timestamps)
            max_serie_size, min_in_top_list = update_series_data(top_n_series, max_serie_size, min_in_top_list,
                                                                 number_of_top_series_to_avg, serie_length)

            results.append([user_id, max_serie_size, mean([i for i in top_n_series if i != 0])])

    return results


#   On input sorted timestamps for each user
def max_messages_number_in_time_window(users_tweets_timestamps):
    results = []
    time_gap = 60 * 5  # 15 min

    for user_id, timestamps in users_tweets_timestamps.items():
        max_msg_number = 0
        i = 0
        while i < len(timestamps):
            timestamps_in_time_window = []
            begin_from = timestamps[i]
            j = i + 1
            while j < len(timestamps):
                next_timestamp = timestamps[j]
                if begin_from + time_gap > next_timestamp:
                    timestamps_in_time_window.append(next)
                    j += 1
                else:
                    break
            msg_number_in_window = len(timestamps_in_time_window)
            if msg_number_in_window > max_msg_number:
                max_msg_number = msg_number_in_window

            i += 1

        results.append([user_id, max_msg_number + 1])   # +1 to count starting message

    return results


def calculate_ratio_follower_following(followers_number, following_number):
    return float(followers_number) / (float(following_number) + 1)


def assign_category_to_twitter_client(tweet_client_name):
    official_clients_mobile = (
        'Twitter for iPhone', 'Twitter for Android', 'Twitter for iPad', 'Twitter for Windows Phone',
        'Twitter for BlackBerry', 'Twitter for Android Tablets', 'Twitter for BlackBerry®')
    official_clients_pc = ('Twitter Web Client', 'Twitter Web App', 'Twitter for Windows', 'Twitter for Mac')
    popular_unofficial = (
        'twitterfeed', 'IFTTT', 'TweetDeck', 'Facebook', 'dlvr.it', 'Linkis: turn sharing into growth', 'Twibble.io')

    if tweet_client_name in official_clients_mobile:
        return 'official-mobile'
    if tweet_client_name in official_clients_pc:
        return 'official-pc'
    elif tweet_client_name in popular_unofficial:
        return 'popular-unofficial'

    return 'unofficial'


def assign_category_to_portal(portal):
    top_news_portals = ('cnn.it', 'hill.cm', 'nyti.ms', 'washingtonpost.com', 'huffingtonpost.com', 'politi.co',
                        'washex.am', 'nytimes.com', 'thehill.com', 'fxn.ws', 'foxnews.com', 'politico.com',
                        'theguardian.com', 'dailycaller.com', 'nbcnews.to', 'cnn.com', 'chicagotribune.com',
                        'cbslocal.com', 'cleveland19.com', 'mysanantonio.com', 'detroitnews.com', 'cleveland.com',
                        'abc7news.com', 'abc7.com', 'dailym.ai', 'nbcchicago.com', 'seattletimes.com',
                        'nbcwashington.com', 'nydailynews.com')
    top_social = ('fb.me', 'instagram.com', 'facebook.com')
    top_media = ('youtu.be', 'youtube.com', 'vine.co', 'vimeo.com')
    top_link_shortener = ('bit.ly', 'ow.ly', 'goo.gl', 'tinyurl.com')

    if portal == 'twitter.com':
        return 'twitter'
    if portal in top_link_shortener:
        return 'shortener'
    if portal in top_news_portals:
        return 'news'
    if portal in top_social:
        return 'social'
    elif portal in top_media:
        return 'media'

    return 'other'


def check_portals_category(portals_list):
    if len(portals_list) == 0:
        return 'none'
    if len(portals_list) > 1:
        return 'multi'

    return assign_category_to_portal(portals_list[0])


def get_user_favorite_client_category_and_clients(data):
    categories_for_multiple_favorite = ('multiple-only-official', 'multiple-only-unofficial', 'multiple-both-categories')
    official_clients_categories = ('official-mobile', 'official-pc', 'multiple-only-official')
    unofficial_client_categories = ('popular-unofficial', 'unofficial', 'multiple-only-unofficial')

    map_user_id_to_result = {}
    for row in data:
        user_id = row[0]
        favorite_tweet_client_name = row[1]
        client_category = assign_category_to_twitter_client(favorite_tweet_client_name)

        if user_id in map_user_id_to_result:
            current_client_name = map_user_id_to_result[user_id][0]
            current_category = map_user_id_to_result[user_id][1]

            current_client_name += ", " + favorite_tweet_client_name
            if current_category == client_category:
                map_user_id_to_result[user_id] = (current_client_name, client_category)
            elif current_category in official_clients_categories and client_category in official_clients_categories:
                map_user_id_to_result[user_id] = (current_client_name, categories_for_multiple_favorite[0])
            elif current_category in unofficial_client_categories and client_category in unofficial_client_categories:
                map_user_id_to_result[user_id] = (current_client_name, categories_for_multiple_favorite[1])
            else:
                map_user_id_to_result[user_id] = (current_client_name, categories_for_multiple_favorite[2])
        else:
            map_user_id_to_result[user_id] = (favorite_tweet_client_name, client_category)

    return map_user_id_to_result


def prepare_tensorflow_graph_and_session():
    #  "https://tfhub.dev/google/universal-sentence-encoder/2" na tym bylo liczone wczesniej
    # module_url = "https://tfhub.dev/google/universal-sentence-encoder-large/5"
    module_url = "https://tfhub.dev/google/universal-sentence-encoder/4"

    g = tf.Graph()
    with g.as_default():
        placeholder = tf.placeholder(dtype=tf.string, shape=[None])
        embed = hub.KerasLayer(module_url)      # KerasLayer   Module
        embedded_placeholder = embed(placeholder)
        init_op = tf.group([tf.global_variables_initializer(), tf.tables_initializer()])
    g.finalize()

    session = tf.Session(graph=g)
    session.run(init_op)

    return session, embedded_placeholder, placeholder


def convert_to_angular_distance(m):
    return 1 - (np.arccos(m) / np.pi)


def check_message_similatiry(session, embedded_text, text_input, tweets_texts_list, similarity_factor):
    if len(tweets_texts_list) <= 1:
        return [0], [0]

    texts_emeddings = session.run(embedded_text, feed_dict={text_input: tweets_texts_list})
    corr = np.inner(texts_emeddings, texts_emeddings)

    corr_removed_diagonal = corr[~np.eye(corr.shape[0], dtype=bool)].reshape(corr.shape[0], -1)
    corr_removed_diagonal[corr_removed_diagonal > 1] = 1  # some values in matrix are little above 1.0 due floating
    # point numbers precision and causes problems in next steps
    corr_angular_distances = convert_to_angular_distance(corr_removed_diagonal)

    means_of_messages_similarity = corr_angular_distances.mean(axis=1)
    similar_messages_numbers = (corr_angular_distances > similarity_factor).sum(axis=1)

    return means_of_messages_similarity, similar_messages_numbers


def perform_message_similarity_analysis(userids_with_tweets, map_tweetid_to_result, similarity_factor):
    map_user_to_tweets = prepare_data(userids_with_tweets)
    session, embedded_placeholder, placeholder = prepare_tensorflow_graph_and_session()

    for user_id, tweets in map_user_to_tweets.items():
        tweets_texts_list = [tweet_text for (tweet_id, tweet_text) in tweets]
        means_of_messages_similarity, similar_messages_numbers = \
            check_message_similatiry(session, embedded_placeholder, placeholder, tweets_texts_list, similarity_factor)

        for i in range(len(tweets_texts_list)):
            tweet_id = tweets[i][0]
            avg_similarity = means_of_messages_similarity[i]
            similar_num = similar_messages_numbers[i]

            map_tweetid_to_result[tweet_id].set_similarity_analysis_result(avg_similarity, similar_num)


def perform_message_similarity_analysis_results_in_lists(userids_with_tweets, similarity_factor):
    map_user_to_tweets = prepare_data(userids_with_tweets)
    session, embedded_placeholder, placeholder = prepare_tensorflow_graph_and_session()

    avg_similarities_list = []
    similar_numbers_list = []

    for user_id, tweets in map_user_to_tweets.items():
        tweets_texts_list = [tweet_text for (tweet_id, tweet_text) in tweets]
        means_of_messages_similarity, similar_messages_numbers = \
            check_message_similatiry(session, embedded_placeholder, placeholder, tweets_texts_list, similarity_factor)

        for i in range(len(tweets_texts_list)):
            avg_similarity = means_of_messages_similarity[i]
            similar_num = similar_messages_numbers[i]

            avg_similarities_list.append(avg_similarity)
            similar_numbers_list.append(similar_num)

    return avg_similarities_list, similar_numbers_list


def perfmorm_graph_analysis_on_retweeted_users(cursor, map_user_to_tweets, switch_to_trolls, retweets_number_above, min_clique_size_to_count):
    if switch_to_trolls:
        query = 'SELECT * FROM (SELECT user_id, retweet_user_id, count(*) as retweets_number FROM tweets WHERE retweet_user_id != \'\' and retweet_user_id is not null GROUP BY user_id, retweet_user_id) as t WHERE t.retweets_number > ' + str(retweets_number_above)
    else:
        query = 'SELECT * FROM (SELECT user_id_str, r_user_id_str, count(*) as retweets_number FROM tweets_n WHERE r_user_id_str != \'\' and r_user_id_str is not null GROUP BY user_id_str, r_user_id_str) as t WHERE retweets_number > ' + str(retweets_number_above)

    graph = nx.Graph()
    users_data = {}

    cursor.execute(query)

    for row in cursor:
        user_id = row[0]
        retweeted_user_id = row[1]
        retweet_number = int(row[2])

        graph.add_edge(str(user_id), str(retweeted_user_id))  # , weight=retweet_number)

        if user_id not in users_data:
            users_data[user_id] = {'maxCliqueSize': 1, 'numberOfCliquesIn': 0}

        if retweeted_user_id not in users_data:
            users_data[retweeted_user_id] = {'maxCliqueSize': 1, 'numberOfCliquesIn': 0}

    maximal_cliques = nx.find_cliques(graph)

    for clique in maximal_cliques:
        for user_id in clique:
            clique_size = len(clique)
            if clique_size >= min_clique_size_to_count:
                users_data[user_id]['numberOfCliquesIn'] += 1

            if users_data[user_id]['maxCliqueSize'] < clique_size:
                users_data[user_id]['maxCliqueSize'] = clique_size

    return {k: v for k, v in users_data.items() if k in map_user_to_tweets}


def init_tokenizer_emotions(max_len):
    with open(VOCAB_PATH, 'r') as f:
        vocabulary = json.load(f)

    st = SentenceTokenizer(vocabulary, max_len)
    model = torchmoji_emojis(PRETRAINED_PATH)

    return st, model


def top_elements(array, k):
    ind = np.argpartition(array, -k)[-k:]
    return ind[np.argsort(array[ind])][::-1]


def perform_text_emotions_analysis(sentences_list, sentence_tokenizer, model):
    elements_to_get = 2500
    results = []
    for iteration_number in range(0, math.ceil(len(sentences_list) / elements_to_get)):
        index = iteration_number * elements_to_get
        sentences_list_part = sentences_list[index:index+elements_to_get]

        sentences = [el[1] for el in sentences_list_part]
        tokenized, _, _ = sentence_tokenizer.tokenize_sentences(sentences)
        prob = model(tokenized)

        for prob in [prob]:
            for id_, t in enumerate(sentences_list_part):
                t_score = [t[0]]
                t_prob = prob[id_]
                ind_top = top_elements(t_prob, 5)
                t_score.append(sum(t_prob[ind_top]))
                t_score.extend(ind_top)
                t_score.extend([t_prob[ind] for ind in ind_top])
                results.append(t_score)

    return results


def append_to_user_tweet_map(map_user_to_tweets, user_id, tweet_id, tweet_text):
    if user_id not in map_user_to_tweets:
        map_user_to_tweets[user_id] = []

    map_user_to_tweets[user_id].append((tweet_id, tweet_text))


def prepare_data(userids_with_tweets):
    map_user_to_tweets = {}
    for elem in userids_with_tweets:
        user_id = elem[0]
        tweet_id = elem[1]
        tweet_text = preprocess_tweet_text_advanced(elem[2])    # preproress_tweet_text_base(elem[2])

        append_to_user_tweet_map(map_user_to_tweets, user_id, tweet_id, tweet_text)

    return map_user_to_tweets


if __name__ == '__main__':

    text_tweet = "This is Rachel Crooks. In 2005 she accused Donald Trump of kissing her on the mouth without her permission.  Now she is running for the state legislature in Ohio. https://t.co/BiFKQe6WVh"

    normal = "RT @realDonaldTrump: Justice Ginsburg of the U.S. Supreme Court has embarrassed all by making very dumb political statements about me. Her…"
    text = "RT @gitagatubixi #Trump Sing along with us: 🎶Better not do us wrong!🎺 https://t.co/NPhXbfZ92g"
    pp = preprocess_tweet_text_advanced(text)
    # re.sub(r'RT @[^ ]*?:', '', text, count=1, flags=re.MULTILINE)
    tt = preprocess_tweet_text_advanced(text_tweet)

    blobber = Blobber(analyzer=NaiveBayesAnalyzer())
    words_number, polarity, subjectivity, tag = stanford_nltk_blob_analysis(text_tweet, blobber)
    x = 5

    tweets_texts_list = ['RT Trump Sing along with us: 🎶Better not do us wrong!🎺', 'RT Trump Sing along with us: 🎶Better not do us wrong!🎺', 'RT LorettoRegina Trump Sing along with us: 🎶We honor our veterans!🎺', 'RT WilliamRolar Trump Sing along with us: 🎶Be bad, you’ll get banned!🎺']
    session, embedded_placeholder, placeholder = prepare_tensorflow_graph_and_session()
    check_message_similatiry(session, embedded_placeholder, placeholder, tweets_texts_list, 0.8)

    # tweet_text = ""
    # tweet_text = re.sub(r'[-a-zA-Z0–9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)', "",
    #                     tweet_text, flags=re.MULTILINE)
    #
    # blobber = Blobber(analyzer=NaiveBayesAnalyzer())
    # words_number, polarity, subjectivity, tag = stanford_nltk_blob_analysis("you're retarded fucking idiot", blobber)
    # words_number_1, polarity_1, subjectivity_1, tag_1 = stanford_nltk_blob_analysis("you\'re retarded fucking IDIOT", blobber)
    # # words_number_, polarity_, subjectivity_, tag_ = stanford_nltk_blob_analysis("you are retarded fucking idiot stupid", blobber)
    #
    # text = "@user #hashtag you\'re retarded fukcing idioot @user #hashtag"
    # print(text)
    # words_number_2, polarity_2, subjectivity_2, tag_2 = stanford_nltk_blob_analysis(text, blobber)
    #
    # text = preprocess_tweet_text_advanced(text)
    # print(text)
    # words_number_x, polarity_x, subjectivity_x, tag_x = stanford_nltk_blob_analysis(text, blobber)

    x = 5
