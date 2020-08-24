import networkx as nx
import psycopg2
from analyze.Utils import *

switchToTrolls = False
file_name = 'graph-analysis-NORM.txt'
min_retweets_number = 5

if __name__ == '__main__':
    G = nx.Graph()
    G.add_node(54)
    maximal_cliques = nx.find_cliques(G)

    connection = psycopg2.connect("dbname=twitter-us-election user=postgres password=1234")
    cursor = connection.cursor()

    if switchToTrolls:
        users_query = 'SELECT user_id FROM tweets GROUP BY user_id'
        query = 'SELECT * FROM (SELECT user_id, retweet_user_id, count(*) as retweets_number FROM tweets WHERE retweet_user_id != \'\' and retweet_user_id is not null GROUP BY user_id, retweet_user_id) as t WHERE t.retweets_number > ' + str(min_retweets_number)
    else:
        users_query = 'SELECT user_id_str FROM tweets_n GROUP BY user_id_str'
        query = 'SELECT * FROM (SELECT user_id_str, r_user_id_str, count(*) as retweets_number FROM tweets_n WHERE r_user_id_str != \'\' and r_user_id_str is not null GROUP BY user_id_str, r_user_id_str) as t WHERE retweets_number > ' + str(min_retweets_number)

    users_from_db = {}
    cursor.execute(users_query)
    for row in cursor:
        users_from_db[row[0]] = row[0]

    # directed graph
    G = nx.Graph()
    users_data = {}

    cursor.execute(query)

    map_id_to_user = {}
    index = 0

    for row in cursor:
        index += 1
        user_id = row[0]
        retweeted_user_id = row[1]
        retweet_number = int(row[2])

        G.add_edge(str(user_id), str(retweeted_user_id))  # , weight=retweet_number)

        if user_id not in users_data:
            users_data[user_id] = {'maxCliqueSize': 0, 'numberOfCliquesIn': 0}

        if retweeted_user_id not in users_data:
            users_data[retweeted_user_id] = {'maxCliqueSize': 0, 'numberOfCliquesIn': 0}

    maximal_cliques = nx.find_cliques(G)

    for clique in maximal_cliques:
        for user_id in clique:
            clique_size = len(clique)
            if clique_size > 2:
                users_data[user_id]['numberOfCliquesIn'] += 1

            if users_data[user_id]['maxCliqueSize'] < clique_size:
                users_data[user_id]['maxCliqueSize'] = clique_size

    filtered = {k: v for k, v in users_data.items() if k in users_from_db}

    bins_clique_size = [0] * 30000

    bins_numbers_cliques_in = list(range(0, 10))
    bins_numbers_cliques_in.extend(get_bins_x10(6)[10:])
    bins_cliques_in = [0] * len(bins_numbers_cliques_in)

    for data in filtered.values():
        maxCliqueSize = data['maxCliqueSize']
        numberOfCliquesIn = data['numberOfCliquesIn']

        bins_clique_size[maxCliqueSize] += 1
        append_to_bin(numberOfCliquesIn, bins_numbers_cliques_in, bins_cliques_in)

    with open(file_name, 'a') as the_file:
        the_file.write("\n".join(str(item) for item in filter_zero_values_from_end(bins_clique_size)))
        the_file.write("\n------------------\n")
        the_file.write("\n".join(str(item) for item in filter_zero_values_from_end(bins_cliques_in)))
