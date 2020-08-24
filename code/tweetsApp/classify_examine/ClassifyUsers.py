import time

import pandas as pd
from sklearn import preprocessing, model_selection
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn.linear_model import LassoCV
from sklearn.metrics import make_scorer, confusion_matrix, accuracy_score
from sklearn.model_selection import cross_val_score, cross_validate, cross_val_predict
from sklearn.multiclass import OneVsRestClassifier
from sklearn.naive_bayes import GaussianNB, BernoulliNB, MultinomialNB
from sklearn.neighbors import KNeighborsClassifier, NearestCentroid
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier, ExtraTreeClassifier
from sklearn.metrics import precision_recall_fscore_support as score
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
import numpy as np
from tabulate import tabulate
from matplotlib import pyplot as plt
import seaborn as sns
import matplotlib
from sklearn.metrics import make_scorer, accuracy_score, precision_score, recall_score, f1_score
from sklearn.linear_model import LogisticRegression
from sklearn import svm

results_file = 'classify-features-single-0208'


def load_data_from_file(file_name):
    tweets_set = set()
    f = open(file_name, "r")

    for line in f:
        splitted = line.split(",")

        user_id = splitted[0].strip()
        tweet_id = splitted[1].strip()
        chars_number = int(splitted[2].strip())
        words_number = int(splitted[3].strip())
        polarity = float(splitted[4].strip())
        subjectivity = float(splitted[5].strip())
        tag = splitted[6].strip()
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
        sum_of_5 = float(splitted[25].strip())
        emotion_nr_1 = int(splitted[26].strip())
        emotion_nr_2 = int(splitted[27].strip())
        emotion_nr_3 = int(splitted[28].strip())
        emotion_nr_4 = int(splitted[29].strip())
        emotion_nr_5 = int(splitted[30].strip())
        emotion_nr_1_part = float(splitted[31].strip())
        emotion_nr_2_part = float(splitted[32].strip())
        emotion_nr_3_part = float(splitted[33].strip())
        emotion_nr_4_part = float(splitted[34].strip())
        emotion_nr_5_part = float(splitted[35].strip())
        label = splitted[36].strip()

        tweets_set.add((
            # user_id,
            tweet_id,
            chars_number,
            words_number,
            polarity,
            subjectivity,
            tag,
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
            sum_of_5,
            emotion_nr_1,
            emotion_nr_2,
            emotion_nr_3,
            emotion_nr_4,
            emotion_nr_5,
            emotion_nr_1_part,
            emotion_nr_2_part,
            emotion_nr_3_part,
            emotion_nr_4_part,
            emotion_nr_5_part,
            label
        ))

    loaded_data = pd.DataFrame(tweets_set)
    loaded_data.columns = [
        # 'user_id',
        'tweet_id',
        'chars_number',
        'words_number',
        'polarity',
        'subjectivity',
        'tag',
        'max_serie_size',
        'urls_number',
        'hashtags_count',
        'user_mentions_count',
        'favorite_count',
        'tweet_client_category',
        'follower_count',
        'following_count',
        'ratio_follower_following',
        'retweeted_user_ratio_follower_following',
        'retweet_maximal_clique_in_size',
        'retweet_maximal_cliques_in_number',
        'top_n_series_avg',
        'max_tweets_number_in_time_window',
        'avg_similarity',
        'num_of_similar_messages',
        'favorite_client_category',
        'url_portal_category',
        'sum_of_5',
        'emotion_nr_1',
        'emotion_nr_2',
        'emotion_nr_3',
        'emotion_nr_4',
        'emotion_nr_5',
        'emotion_nr_1_part',
        'emotion_nr_2_part',
        'emotion_nr_3_part',
        'emotion_nr_4_part',
        'emotion_nr_5_part',
        'label'
    ]

    return loaded_data


def single_feature_classification_results(tweets, target, classifier):
    with open(results_file, 'a', encoding="utf-8") as results_file_:
        for i in range(0, len(tweets.columns) - 10):
            if i < 23:
                single_feature_data = tweets[tweets.columns[i]]
                column_name = single_feature_data.name
                single_feature_data = single_feature_data.values.reshape(len(single_feature_data), 1)
            elif i == 23:
                single_feature_data = tweets[
                    ['sum_of_5', 'emotion_nr_1', 'emotion_nr_2', 'emotion_nr_3', 'emotion_nr_4',
                     'emotion_nr_5', 'emotion_nr_1_part', 'emotion_nr_2_part', 'emotion_nr_3_part',
                     'emotion_nr_4_part', 'emotion_nr_5_part']]
                column_name = 'emotions'

            print(column_name)
            precision, recall, fscore, accuracy, roc_auc = learn_and_predict(single_feature_data, target, classifier)
            write_single_result_to_file(results_file_, column_name, precision, recall, fscore, accuracy, roc_auc)


def users_classification_agreement_between_single_features(tweets, target, classifier):
    list_of_predictions_for_features = []

    with open(results_file, 'a', encoding="utf-8") as the_file:
        for i in range(0, len(tweets.columns) - 10):
            if i < 23:
                single_feature_data = tweets[tweets.columns[i]]
                column_name = single_feature_data.name
                single_feature_data = single_feature_data.values.reshape(len(single_feature_data), 1)
            elif i == 23:
                single_feature_data = tweets[
                    ['sum_of_5', 'emotion_nr_1', 'emotion_nr_2', 'emotion_nr_3', 'emotion_nr_4',
                     'emotion_nr_5', 'emotion_nr_1_part', 'emotion_nr_2_part', 'emotion_nr_3_part',
                     'emotion_nr_4_part', 'emotion_nr_5_part']]
                column_name = 'emotions'

            predictions_ = cross_val_predict(classifier, single_feature_data, target, cv=10, n_jobs=6)

            list_of_predictions_for_features.append(predictions_)

            precision, recall, fscore, support = score(target, predictions_, average='macro')
            # confusion_matrix = confusion_matrix(target, predictions_)
            accuracy = accuracy_score(target, predictions_)

            the_file.write("\n" + column_name + ":\nF1 score: " + str(fscore) + "\n" + str(precision) + "\n" + str(
                recall) + "\n" + str(accuracy))

    # if label 1 = normal user
    number_of_normal = sum(target)
    number_of_trolls = len(target) - number_of_normal

    results_table_trolls = []
    results_table_normal = []
    for index, checked_element in enumerate(list_of_predictions_for_features):
        number_of_all_classified_as_trolls = sum(np.logical_not(checked_element))
        number_of_all_classified_as_normal = sum(checked_element)

        percentage_trolls = []
        percentage_normal = []

        for element in list_of_predictions_for_features:
            same_troll_predictions = np.logical_not(np.logical_or(checked_element, element))
            same_normal_predictions = np.logical_and(checked_element, element)

            same_correct_troll_predictions = np.logical_and(same_troll_predictions, np.logical_not(target))
            same_correct_normal_prediction = np.logical_and(same_normal_predictions, target)

            number_of_same_correct_troll_predictions = sum(same_correct_troll_predictions)
            number_of_same_correct_normal_predictions = sum(same_correct_normal_prediction)

            percentage_trolls.append((number_of_same_correct_troll_predictions / number_of_trolls) * 100)
            percentage_normal.append((number_of_same_correct_normal_predictions / number_of_normal) * 100)

        results_table_trolls.append(percentage_trolls)
        results_table_normal.append(percentage_normal)

    with open(results_file, 'a', encoding="utf-8") as the_file:
        the_file.write("\nN:\n")
        the_file.write(tabulate(results_table_trolls))
        the_file.write("\nT:\n")
        the_file.write(tabulate(results_table_normal))


def get_wrong_classified_tweets_ids(tweets, target, tweets_ids, clf=RandomForestClassifier()):
    predictions = cross_val_predict(clf, tweets, target, cv=10, n_jobs=-1)

    precision, recall, fscore, support = score(target, predictions, average='macro')
    accuracy = accuracy_score(target, predictions)

    print("Precision: " + str(precision))
    print("Recall: " + str(recall))
    print("F1: " + str(fscore))
    print("Accuracy: " + str(accuracy))

    conf_mat = confusion_matrix(target, predictions)
    print("\nConfusion matrix:\n")
    print(conf_mat)

    wrong_classified_unwanted, wrong_classified_normal = [], []
    for target_, prediction_, t_id in zip(target, predictions, tweets_ids):
        if target_ == 1 and prediction_ == 0:
            wrong_classified_unwanted.append(t_id)
        elif target_ == 0 and prediction_ == 1:
            wrong_classified_normal.append(t_id)

    with open("outfile-wrong-unwanted", "w") as outfile:
        outfile.write("\n".join(wrong_classified_unwanted))
    with open("outfile-wrong-normal", "w") as outfile:
        outfile.write("\n".join(wrong_classified_normal))

    return wrong_classified_unwanted, wrong_classified_normal


def learn_and_predict(tweets, target, clf=RandomForestClassifier()):
    kfold = model_selection.KFold(n_splits=10, random_state=42, shuffle=True)

    results_bin = cross_validate(estimator=clf,
                                 X=tweets,
                                 y=target,
                                 cv=kfold,
                                 scoring=('accuracy', 'precision', 'recall', 'f1', 'roc_auc'),
                                 n_jobs=5)

    precision = np.mean(results_bin['test_precision'])
    recall = np.mean(results_bin['test_recall'])
    fscore = np.mean(results_bin['test_f1'])
    accuracy = np.mean(results_bin['test_accuracy'])
    roc_auc = np.mean(results_bin['test_roc_auc'])

    return precision, recall, fscore, accuracy, roc_auc


def all_with_remove_only_one_feature(tweets, target, classifier, results_file_all_except):
    # ignore emotions participation
    # tweets = tweets[tweets.columns[:-5]]

    # tweets = tweets[[
    #     # 'urls_number',
    #     # 'hashtags_count',
    #     # 'user_mentions_count',
    #     # 'favorite_count',
    #     'following_count',
    #     'ratio_follower_following',
    #     # 'retweeted_user_ratio_follower_following',
    #     'retweet_maximal_clique_in_size',
    #     # 'retweet_maximal_cliques_in_number',
    #     'top_n_series_avg',
    #     # 'avg_similarity',
    #     # 'num_of_similar_messages',
    #     'favorite_client_category',
    #     # 'url_portal_category',
    #     # 'emotion_nr_4',
    #     # 'emotion_nr_5',
    #     'follower_count',
    #     'max_serie_size',
    #     'max_tweets_number_in_time_window'
    #     # 'tweet_client_category'
    # ]]

    # tweets = tweets[[
    #     'following_count',
    #     'ratio_follower_following',
    #     'retweet_maximal_clique_in_size',
    #     'retweet_maximal_cliques_in_number',
    #     'top_n_series_avg',
    #     'favorite_client_category',
    #     'follower_count',
    #     'max_serie_size',
    #     'max_tweets_number_in_time_window'
    # ]]

    # tweets = tweets[[
    #     'chars_number',
    #     'words_number',
    #     'subjectivity',
    #     'tag',
    #     'urls_number',
    #     'hashtags_count',
    #     'user_mentions_count',
    #     'favorite_count',
    #     'retweet_maximal_clique_in_size',
    #     'retweet_maximal_cliques_in_number',
    #     'num_of_similar_messages',
    #     'url_portal_category'
    # ]]

    tweets = tweets[[
        'chars_number',
        'words_number',
        'subjectivity',
        'tag',
        # 'urls_number',
        'hashtags_count',
        'user_mentions_count',
        'favorite_count',
        'retweet_maximal_clique_in_size',
        'retweet_maximal_cliques_in_number',
        'num_of_similar_messages',
        'url_portal_category'
    ]]

    results = []
    for column_except in tweets.columns:  # tweets.columns[:-10]:
        print(column_except)
        if column_except != 'sum_of_5':
            all_except_single_feature = tweets.loc[:, tweets.columns != column_except]
        else:
            all_except_single_feature = tweets[tweets.columns[:-6]]

        precision, recall, fscore, accuracy, roc_auc = learn_and_predict(all_except_single_feature, target, classifier)
        results.append([column_except, precision, recall, fscore, accuracy])

    results.sort(key=lambda x: x[3], reverse=True)

    with open(results_file_all_except, 'a', encoding="utf-8") as the_file:
        for result in results:
            the_file.write(",".join(str(item) for item in result) + "\n")


def pearson_correlation(data):
    plt.figure(figsize=(12, 10))
    cor = data.corr()

    corr_abs = cor.abs()
    filtered = (
        corr_abs.where(np.triu(np.ones(corr_abs.shape), k=1).astype(np.bool)).stack().sort_values(ascending=False))

    filtered_df = filtered.to_frame().reset_index()
    filtered_df["corr_label_first"] = np.nan
    filtered_df["corr_label_sec"] = np.nan

    correlation_with_label = cor.iloc[:, -1]
    for index, row in filtered_df.iterrows():
        filtered_df.at[index, 'corr_label_first'] = correlation_with_label[row['level_0']]
        filtered_df.at[index, 'corr_label_sec'] = correlation_with_label[row['level_1']]

    filtered_df.to_csv("a-correlations11.txt")

    sns.heatmap(cor, annot=False, cmap="YlGnBu")
    plt.savefig('aa-pearson-heatmap.png')
    plt.show()


def lasso(tweets, target):
    tweets.drop('following_count', axis=1, inplace=True)
    tweets.drop('follower_count', axis=1, inplace=True)
    tweets.drop('retweeted_user_ratio_follower_following', axis=1, inplace=True)
    # tweets.drop('retweet_maximal_cliques_in_number', axis=1, inplace=True)
    #
    tweets.drop('ratio_follower_following', axis=1, inplace=True)
    # tweets.drop('retweet_maximal_clique_in_size', axis=1, inplace=True)

    # tweets = tweets[['emotion_nr_1_part',
    #                  'emotion_nr_2_part',
    #                  'emotion_nr_3_part',
    #                  'emotion_nr_4_part',
    #                  'emotion_nr_5_part',
    #                  'sum_of_5',
    #                  'tag',
    #                  'words_number',
    #                  'polarity',
    #                  'subjectivity',
    #                  'retweet_maximal_clique_in_size',
    #                  'avg_similarity'
    #                  ]]

    lasso_ = LassoCV()
    lasso_.fit(tweets, target)
    coef = pd.Series(lasso_.coef_, index=tweets.columns)

    choosen_number = sum(coef != 0)
    redundant_number = sum(coef == 0)
    print("Choosen: " + str(choosen_number))
    print("Redundant: " + str(redundant_number))
    print(coef.abs().where(coef != 0).sort_values(ascending=False).dropna())

    matplotlib.rcParams['figure.figsize'] = (8.0, 10.0)
    coef.sort_values().plot(kind="barh")
    plt.title("Współczynniki cech w modelu Lasso.")
    plt.show()


def write_single_result_to_file(output_file, features_list, precision, recall, fscore, accuracy, roc_auc):
    output_file.write("Features: " + features_list.strip() + "\n"
                      + "Precision: " + str(precision)
                      + "\nRecall: " + str(recall)
                      + "\nFscore: " + str(fscore)
                      + "\nAccuracy: " + str(accuracy)
                      + "\nRoc_auc: " + str(roc_auc)
                      + "\n" + " ".join([str(x) for x in (fscore, precision, recall, accuracy, roc_auc)])
                      + "\n\n")


def run_features_from_file(tweets, target, classifier, choosen_features_file):
    output_file = get_output_file_name_with_date_and_time('choosen_features_results_output')
    with open(choosen_features_file, 'r', encoding="utf-8") as choosen_features_file_, \
            open(output_file, 'w', encoding="utf-8") as output_file_:
        for features in choosen_features_file_:
            print(features)
            choosen_features_names = [feature_name.strip() for feature_name in features.split(",")]
            subset_features_data = tweets[choosen_features_names]

            precision, recall, fscore, accuracy, roc_auc = learn_and_predict(subset_features_data, target, classifier)
            write_single_result_to_file(output_file_, features, precision, recall, fscore, accuracy, roc_auc)


def get_output_file_name_with_date_and_time(prefix):
    timestr = time.strftime("%Y%m%d-%H%M%S")
    return prefix + '-' + timestr + '.txt'


def compare_different_classifiers_results(tweets, target):
    # # 8 cech metoda eliminacji
    # tweets = tweets[[
    #     'max_serie_size',
    #     'follower_count',
    #     'ratio_follower_following',
    #     'following_count',
    #     'max_tweets_number_in_time_window',
    #     'retweet_maximal_clique_in_size',
    #     'top_n_series_avg',
    #     'favorite_client_category'
    # ]]

    # Pearson + obserwujacy
    tweets = tweets[[
        'chars_number',
        'polarity',
        'subjectivity',
        'urls_number',
        'hashtags_count',
        'user_mentions_count',
        'favorite_count',
        'follower_count',
        'following_count',
        'ratio_follower_following',
        'retweeted_user_ratio_follower_following',
        'retweet_maximal_clique_in_size',
        'retweet_maximal_cliques_in_number',
        'top_n_series_avg',
        'avg_similarity',
        'num_of_similar_messages',
        'favorite_client_category',
        'url_portal_category',
        'emotion_nr_1',
        'emotion_nr_2',
        'emotion_nr_3',
        'emotion_nr_4',
        'emotion_nr_5'
    ]]

    classifiers = [
        # ExtraTreeClassifier(),
        # DecisionTreeClassifier(),
        # RandomForestClassifier(),
        # MLPClassifier(alpha=1, max_iter=1000),
        # AdaBoostClassifier(),
        # GaussianNB(),
        # BernoulliNB(),
            # MultinomialNB(),
        LogisticRegression(),
        # KNeighborsClassifier(7),
        # KNeighborsClassifier(5),
        KNeighborsClassifier(3)
        # OneVsRestClassifier(SVC(kernel='linear', probability=True), n_jobs=-1)
    ]

    output_file = get_output_file_name_with_date_and_time('classifiers-comparison')
    with open(output_file, 'w', encoding="utf-8") as output_file_:
        for clf in classifiers:
            name = type(clf).__name__
            print(name)
            precision, recall, fscore, accuracy, roc_auc = learn_and_predict(tweets, target, clf)
            write_single_result_to_file(output_file_, name, precision, recall, fscore, accuracy, roc_auc)


if __name__ == '__main__':
    # normal dataset
    tweets = load_data_from_file('createdatasets/final0108bezdodawania')
    # tweets = load_data_from_file('createdatasets/svm100k')
    # dataset with only retweets
    # tweets = load_data_from_file('createdatasets/only-retweets')

    le = preprocessing.LabelEncoder()
    tweets['tag'] = le.fit_transform(tweets['tag'])
    tweets['tweet_client_category'] = le.fit_transform(tweets['tweet_client_category'])
    tweets['favorite_client_category'] = le.fit_transform(tweets['favorite_client_category'])
    tweets['url_portal_category'] = le.fit_transform(tweets['url_portal_category'])
    tweets['label'] = le.fit_transform(tweets['label'])

    tweets_ids = tweets['tweet_id']
    target = tweets['label']

    tweets.drop('label', axis=1, inplace=True)
    tweets.drop('tweet_id', axis=1, inplace=True)

    # pearson_correlation(tweets)
    # lasso(tweets, target)

    # clf = RandomForestClassifier()  # DecisionTreeClassifier()
    # single_feature_classification_results(tweets, target, clf)
    # run_features_from_file(tweets, target, clf, "testfile432")
    # run_classifier_for_each_feature(tweets, target, clf)
    # get_wrong_classified_tweets_ids(tweets, target, tweets_ids)
    # all_with_remove_only_one_feature(tweets, target, clf, "result-all-features-except-worse12-R2")

    compare_different_classifiers_results(tweets, target)
