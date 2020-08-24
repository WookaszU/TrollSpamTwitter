
def load_emotions_results_data(emotions_data_file):
    tweetid_to_emotions_analysis_results = {}
    f = open(emotions_data_file, "r")

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

        tweetid_to_emotions_analysis_results[tweet_id] = [sum_of_5, emotion_nr_1, emotion_nr_2, emotion_nr_3,
                                                          emotion_nr_4, emotion_nr_5,
                                                          emotion_nr_1_part, emotion_nr_2_part, emotion_nr_3_part,
                                                          emotion_nr_4_part, emotion_nr_5_part]

    return tweetid_to_emotions_analysis_results


def append_emotions_results_to_main_file(analyses_file, emotions_file, output_file):
    tweetid_to_emotions_analysis_results = load_emotions_results_data(emotions_file)

    with open(analyses_file, 'r', encoding="utf-8") as analyses_file_, open(output_file, 'w', encoding="utf-8") as output_file_:
        for line in analyses_file_:
            splitted = line.split(",")
            tweet_id = splitted[1].strip()
            try:
                splitted[-1:-1] = tweetid_to_emotions_analysis_results[tweet_id]
                output_file_.write(','.join(str(elem) for elem in splitted))
            except KeyError:
                print(tweet_id)


if __name__ == '__main__':
    # Normal users
    append_emotions_results_to_main_file(analyses_file="normal-final-2807",
                                         emotions_file="emotions_out_normal.txt",
                                         output_file="final-concat-normal-2807.txt")

    # Unwanted users
    # append_emotions_results_to_main_file(analyses_file="new-users-data-ira-out2807new.txt",
    #                                      emotions_file="emotions_out_troll.txt",
    #                                      output_file="final-concat-troll-2807.txt")
