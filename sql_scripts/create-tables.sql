-- Create table
create table tweets(
    Id SERIAL PRIMARY KEY NOT NULL,
    tweet_id VARCHAR(100),
    user_id VARCHAR(100),
    user_display_name VARCHAR(100),
    user_screen_name VARCHAR(100),
    user_reported_location VARCHAR(100),
    user_profile_description VARCHAR(400),
    user_profile_url VARCHAR(100),
    follower_count INTEGER,
    following_count INTEGER,
    account_creation_date DATE,
    account_language VARCHAR(20),
    tweet_language VARCHAR(20),
    tweet_text VARCHAR(500),
    tweet_time TIMESTAMP,
    tweet_client_name VARCHAR(50),
    in_reply_to_tweet_id VARCHAR(100),
    in_reply_to_user_id VARCHAR(100),
    quoted_tweet_tweet_id VARCHAR(100),
    is_retweet BOOLEAN,
    retweet_user_id VARCHAR(100),
    retweet_tweet_id VARCHAR(100),
    latitude VARCHAR(20),
    longitude VARCHAR(20),
    quote_count INTEGER,
    reply_count INTEGER,
    like_count INTEGER,
    retweet_count INTEGER,
    hashtags VARCHAR(200),
    urls VARCHAR(400),
    user_mentions VARCHAR(2000),
    poll_choices VARCHAR(200)
);

-- ---------------------------------------------------------------------------------------------------------------------

create table tweets_n
(
    created_at                  TIMESTAMP,
    hashtags                    VARCHAR(900),
    symbols                     VARCHAR(900),
    user_mentions               VARCHAR(900),
    urls                        VARCHAR(900),
    hashtags_count              INTEGER,
    symbols_count               INTEGER,
    user_mentions_count         INTEGER,
    urls_count                  INTEGER,

    favorite_count              INTEGER,
    id_str                      VARCHAR(100),
    in_reply_to_status_id_str   VARCHAR(100),
    in_reply_to_user_id_str     VARCHAR(100),
    is_quote_status             BOOLEAN,

    lang                        VARCHAR(10),
    place                       VARCHAR(300),
    coordinates                 VARCHAR(120),
    retweet_count               INTEGER,
    retweeted                   BOOLEAN,
    source                      VARCHAR(60),
    text                        VARCHAR(400),
    truncated                   BOOLEAN,

    user_created_at             TIMESTAMP,
    user_default_profile        BOOLEAN,
    user_description            VARCHAR(300),
    user_favourites_count       INTEGER,
    user_followers_count        INTEGER,
    user_friends_count          INTEGER,
    user_has_extended_profile   BOOLEAN,
    user_id_str                 VARCHAR(100),
    user_lang                   VARCHAR(10),
    user_location               VARCHAR(300),
    user_statuses_count         INTEGER,
    user_verified               BOOLEAN,


    q_created_at                TIMESTAMP,
    q_hashtags                  VARCHAR(900),
    q_symbols                   VARCHAR(900),
    q_user_mentions             VARCHAR(900),
    q_urls                      VARCHAR(900),
    q_hashtags_count            INTEGER,
    q_symbols_count             INTEGER,
    q_user_mentions_count       INTEGER,
    q_urls_count                INTEGER,


    q_favorite_count            INTEGER,
    q_id_str                    VARCHAR(100),
    q_is_quote_status           BOOLEAN,

    q_lang                      VARCHAR(10),
    q_place                     VARCHAR(300),
    q_coordinates               VARCHAR(120),
    q_retweet_count             INTEGER,
    q_retweeted                 BOOLEAN,
    q_source                    VARCHAR(60),
    q_text                      VARCHAR(400),
    q_truncated                 BOOLEAN,


    q_user_created_at           TIMESTAMP,
    q_user_default_profile      BOOLEAN,
    q_user_description          VARCHAR(300),
    q_user_favourites_count     INTEGER,
    q_user_followers_count      INTEGER,
    q_user_friends_count        INTEGER,
    q_user_has_extended_profile BOOLEAN,
    q_user_id_str               VARCHAR(100),
    q_user_lang                 VARCHAR(10),
    q_user_location             VARCHAR(300),
    q_user_statuses_count       INTEGER,
    q_user_verified             BOOLEAN,


    r_created_at                TIMESTAMP,
    r_hashtags                  VARCHAR(900),
    r_symbols                   VARCHAR(900),
    r_user_mentions             VARCHAR(900),
    r_urls                      VARCHAR(900),
    r_hashtags_count            INTEGER,
    r_symbols_count             INTEGER,
    r_user_mentions_count       INTEGER,
    r_urls_count                INTEGER,


    r_favorite_count            INTEGER,
    r_id_str                    VARCHAR(100),
    r_is_quote_status           BOOLEAN,

    r_lang                      VARCHAR(10),
    r_place                     VARCHAR(300),
    r_coordinates               VARCHAR(120),
    r_retweet_count             INTEGER,
    r_retweeted                 BOOLEAN,
    r_source                    VARCHAR(60),
    r_text                      VARCHAR(400),
    r_truncated                 BOOLEAN,


    r_user_created_at           TIMESTAMP,
    r_user_default_profile      BOOLEAN,
    r_user_description          VARCHAR(300),
    r_user_favourites_count     INTEGER,
    r_user_followers_count      INTEGER,
    r_user_friends_count        INTEGER,
    r_user_has_extended_profile BOOLEAN,
    r_user_id_str               VARCHAR(100),
    r_user_lang                 VARCHAR(10),
    r_user_location             VARCHAR(300),
    r_user_statuses_count       INTEGER,
    r_user_verified             BOOLEAN,

    Id SERIAL PRIMARY KEY NOT NULL
);


CREATE INDEX user_id_str_idx ON tweets_n (user_id_str);


SELECT nspname || '.' || relname AS "relation",
    pg_size_pretty(pg_relation_size(C.oid)) AS "size"
  FROM pg_class C
  LEFT JOIN pg_namespace N ON (N.oid = C.relnamespace)
  WHERE nspname NOT IN ('pg_catalog', 'information_schema')
  ORDER BY pg_relation_size(C.oid) DESC
  LIMIT 100;
