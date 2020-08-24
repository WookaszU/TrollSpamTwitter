
-- liczba uzytkownikow w zbiorze
SELECT COUNT(*)
FROM
(SELECT DISTINCT tweets_normal.user_id_str
FROM tweets_normal) as i;

SELECT COUNT(*)
FROM
(SELECT DISTINCT user_id
FROM tweets where tweet_language = 'en') as i;

-- 1859531

-- liczba zweryfikowanych uzytkownikow w zbiorze
SELECT COUNT(*)
FROM
(SELECT DISTINCT tweets_normal.user_id_str
FROM tweets_normal
WHERE user_verified is true) as i;

-- 34277

-- followers per number
SELECT max_followers, count(*)
FROM (
SELECT max(user_followers_count) as max_followers, user_id_str
from tweets_n
group by user_id_str) as tt
GROUP BY max_followers
ORDER BY max_followers;

-- 1859531
select count(*)
from
(select distinct user_id_str from tweets_n) as tt;

-- following per number
SELECT max_friends, count(*)
FROM (
SELECT max(user_friends_count) as max_friends, user_id_str
from tweets_n
group by user_id_str) as tt
GROUP BY max_friends
ORDER BY max_friends;

-- 31 355
select count(*) from tweets_normal where user_followers_count = 0;

select count(*) from tweets_n;
select max(following_count) from tweets

SELECT hashtags_count, count(*) as count
from tweets_n
group by hashtags_count
order by hashtags_count;

SELECT user_mentions_count, count(*) as count
from tweets_n
group by user_mentions_count
order by user_mentions_count;

SELECT urls_count, count(*) as count
from tweets
where tweet_language = 'en'
group by urls_count
order by urls_count;

SELECT urls_count, count(*) as count
from tweets_n
where lang = 'en'
group by urls_count
order by urls_count;

SELECT favorite_count, count(*) as count
from tweets_n
group by favorite_count
order by favorite_count;


select count(*) from tweets where urls != '[]' and urls != '';
select count(*) from tweets; -- 1825877
select count(*) from tweets where tweet_language = 'en'; -- 595823


-- followers followeees ratio

SELECT user_id_str, user_description, user_followers_count, user_friends_count, CAST(user_followers_count AS float) / NULLIF(CAST(user_friends_count AS float), 0) as Ratio
FROM tweets_normal
WHERE user_friends_count != 0
GROUP BY user_id_str, user_description, user_followers_count, user_friends_count
order by Ratio desc;

SELECT user_id_str, user_description, floor(MAX(ratio)) as Ratio_
FROM
(SELECT user_id_str, user_description, user_followers_count, user_friends_count, CAST(user_followers_count AS float) / NULLIF(CAST(user_friends_count AS float), 0) as Ratio
FROM tweets_normal
WHERE user_friends_count != 0
GROUP BY user_id_str, user_description, user_followers_count, user_friends_count
order by Ratio desc) as i
GROUP BY user_id_str, user_description
order by Ratio_;

SELECT AVG(Ratio_)
FROM
(SELECT user_id_str, user_description, MAX(ratio) as Ratio_
FROM
(SELECT user_id_str, user_description, user_followers_count, user_friends_count, CAST(user_followers_count AS float) / NULLIF(CAST(user_friends_count AS float), 0) as Ratio
FROM tweets_normal
WHERE user_friends_count != 0
GROUP BY user_id_str, user_description, user_followers_count, user_friends_count
order by Ratio desc) as i
GROUP BY user_id_str, user_description
order by Ratio_ desc) as ii
WHERE Ratio_ is not NULL;


select count(*) from tweets_normal;

SELECT q_id_str FROM tweets_normal
WHERE q_id_str is not NULL;


SELECT min(created_at) FROM tweets_normal;
SELECT max(created_at) FROM tweets_normal;

select id
from tweets_normal
where id is null;

select * FROM tweets_normal
WHERE id_str = '777849142626443265';

SELECT * FROM tweets_normal
ORDER BY id DESC;

SELECT * FROM tweets_normal
WHERE user_id_str = '172858784';

SELECT lang, count(*) as count
from tweets_normal
group by lang
order by count desc;

SELECT tweet_language, count(*) as count
from tweets
group by tweet_language
order by count desc;

SELECT * FROM tweets
WHERE user_id = '3729867851';


SELECT COUNT(*)
FROM tweets
WHERE following_count = 0;

SELECT user_id, user_display_name, user_profile_description, user_screen_name, follower_count, following_count, CAST(follower_count AS float) / NULLIF(CAST(following_count AS float), 0) as Ratio
FROM tweets
WHERE following_count != 0
GROUP BY user_id, follower_count, following_count, user_display_name, user_profile_description,  user_screen_name
order by Ratio desc;

SELECT AVG(Ratio)
FROM (SELECT follower_count, following_count, CAST(follower_count AS float) / NULLIF(CAST(following_count AS float), 0) as Ratio
        FROM tweets
        WHERE following_count != 0 and tweet_language = 'en'
        GROUP BY user_id, follower_count, following_count, user_display_name
        order by Ratio desc) AS RatioGet
WHERE Ratio is not NULL;


select count(*) FROM tweets_normal_old;


select tweet_id, user_mentions, tweet_text, LENGTH(tweet_text) as len from tweets where tweet_language = 'en' order by len desc;

select id_str, text, length(text) as len from tweets_normal_old where lang = 'en' order by len desc;


select count(*) from tweets where hashtags_count is NULL;


SELECT hashtags_count, count(*) as count
from tweets
group by hashtags_count
order by hashtags_count;

SELECT user_mentions_count, count(*) as count
from tweets
group by user_mentions_count
order by user_mentions_count;

SELECT urls_count, count(*) as count
from tweets
group by urls_count
order by urls_count;


SELECT id, id_str, text from tweets_normal where lang = 'en' limit 5;


SELECT id, tweet_id, tweet_text FROM tweets WHERE tweet_language = 'en'

select count(*) from tweets_normal
group by user_id_str

SELECT SUM(urls_count)
FROM tweets_normal
WHERE lang = 'en';

SELECT COUNT(*)
FROM tweets_normal
WHERE lang = 'en' AND urls_count > 0;


-- analiza frequency tweetowania

SELECT user_created_at, max(created_at), count(*) as tweets_number, date(max(created_at)) - date(user_created_at) as days_active
FROM tweets_n
GROUP BY user_id_str, user_created_at;


SELECT user_id_str, tweets_number, days_active, days_active::float8 / tweets_number::float8 as tweeting_frequency, account_creation_date, last_activity_date
FROM (
SELECT user_id_str, user_created_at as account_creation_date, max(created_at) as last_activity_date, count(*) as tweets_number, date(max(created_at)) - date(user_created_at) as days_active
FROM tweets_normal
GROUP BY user_id_str, user_created_at) as i
order by tweeting_frequency desc;


SELECT *
FROM tweets_normal
WHERE user_id_str = '56';

SELECT source, count(*) as counter
FROM tweets_n
where lang = 'en'
GROUP BY source
order by counter desc;

select count(*)
from tweets_n
where lang = 'en'


SELECT source, count(*) as counter
FROM tweets_normal
WHERE source in ('vavilonX', 'newtwittersky', 'Jerusalem')
GROUP BY source
order by counter desc;

select user_id_str, created_at, id_str
from tweets_normal
group by user_id_str, created_at, id_str
order by created_at;




-- IRA

-- followers per number
SELECT follower_count, count(*)
FROM (
SELECT follower_count, user_id
from tweets
group by user_id, follower_count
order by follower_count) as i
GROUP BY follower_count
ORDER BY follower_count;

-- following per number
SELECT following_count, count(*)
FROM (
SELECT following_count, user_id
from tweets
group by user_id, following_count
order by following_count) as i
GROUP BY following_count
ORDER BY following_count;

-- user accounts
SELECT COUNT(*)
FROM
(SELECT DISTINCT user_id
FROM tweets) as i;


-- urls  followers/ followees
SELECT user_id, user_display_name, user_profile_description, user_screen_name, follower_count, following_count, (CAST(follower_count AS float) / NULLIF(CAST(following_count AS float), 0)) as Ratio
FROM tweets
WHERE following_count != 0
GROUP BY user_id, follower_count, following_count, user_display_name, user_profile_description,  user_screen_name
order by Ratio;


SELECT AVG(Ratio)
FROM (SELECT follower_count, following_count, CAST(follower_count AS float) / NULLIF(CAST(following_count AS float), 0) as Ratio
        FROM tweets
        WHERE following_count != 0 and tweet_language = 'en'
        GROUP BY user_id, follower_count, following_count, user_display_name
        order by Ratio desc) AS RatioGet
WHERE Ratio is not NULL;


SELECT SUM(urls_count)
FROM tweets
WHERE tweet_language = 'en';

SELECT COUNT(*)
FROM tweets
WHERE tweet_language = 'en' AND urls_count > 0;



SELECT MAX(user_mentions_count)
FROM tweets_normal;


SELECT Ratio, AVG(follower_count) FROM
(SELECT floor(CAST(follower_count AS float) / NULLIF(CAST(following_count AS float), 0)) as Ratio, follower_count
FROM tweets WHERE following_count != 0
GROUP BY user_id, follower_count, following_count, user_display_name, user_profile_description,  user_screen_name
) as i
GROUP BY Ratio
order by Ratio;



-- analiza frequency tweetowania
SELECT user_id, account_creation_date, count(*) as tweets_number, date(max(tweet_time)) - account_creation_date as days_active
FROM tweets
GROUP BY user_id, account_creation_date;

SELECT user_id, tweets_number, days_active, days_active::float8 / tweets_number::float8 as tweeting_frequency, account_creation_date, last_activity_date
FROM (
SELECT user_id, account_creation_date, date(max(tweet_time)) as last_activity_date, count(*) as tweets_number, date(max(tweet_time)) - account_creation_date as days_active
FROM tweets
GROUP BY user_id, account_creation_date) as i
order by tweeting_frequency;


select tweet_client_name, count(*) as counter
from tweets
--WHERE tweet_language = 'en' -- AND tweet_client_name in ('Twitter for iPhone', 'Twitter for iPad', 'Twitter Web App', 'Facebook', 'dlvr.it')
where tweet_client_name = 'Facebook' and tweet_language = 'en'
GROUP BY tweet_client_name
order by counter desc;

select user_id, tweet_time, tweet_id
from tweets
where tweet_language = 'en'
group by user_id, tweet_time, tweet_id
order by tweet_time;


select user_id, tweet_time::DATE as dat, count(*) as cc
from tweets
where user_id = 'e39056f8a6ed87cda6bc22cbfff630425677170a2fdd21aa132e158eec50d19e'
group by user_id, dat
order by cc desc;

-- 2570574680

SELECT COUNT(*)
FROM tweets
WHERE tweet_language = 'en'
GROUP BY user_id;

SELECT tweets.user_id, COUNT(user_id) AS tweets_count
FROM tweets
WHERE tweet_language = 'en'
GROUP BY user_id
ORDER BY tweets_count DESC;

SELECT *
FROM tweets
ORDER BY follower_count DESC;

SELECT *
FROM tweets
ORDER BY following_count DESC;

SELECT in_reply_to_tweet_id
FROM tweets
WHERE in_reply_to_tweet_id IS NOT NULL and in_reply_to_tweet_id != '';

SELECT *
FROM tweets
WHERE tweet_id = '631191650413465600';

-- --------------------------------------------------------------------------------------------------------------------------------------------------
SELECT user_id, tweet_id FROM tweets WHERE tweet_language = 'en' AND user_id in ('2951506251', '2943515140') limit 10



SELECT user_id, follower_count, following_count  FROM tweets;
SELECT user_id_str, user_followers_count, user_friends_count  FROM tweets_normal;


SELECT user_id FROM (
                                                           SELECT user_id,
                                                                  account_creation_date,
                                                                  date(max(tweet_time)) as last_activity_date,
                                                                  count(*)              as tweets_number
                                                           FROM tweets
                                                           WHERE tweet_language = 'en'
                                                           GROUP BY user_id, account_creation_date, tweet_language
                                                       ) as i
WHERE tweets_number > 20;

SELECT user_id_str, user_created_at, tweets_number FROM (
                                                            SELECT user_id_str,
                                                                   user_created_at,
                                                                   max(created_at),
                                                                   count(*) as tweets_number
                                                            FROM tweets_normal
                                                            WHERE lang = 'en'
                                                            GROUP BY user_id_str, user_created_at
) as i
WHERE tweets_number > 20;




SELECT * FROM tweets WHERE user_id = '02c9129548e92a2052f616144b1691703433e10308996993c1f1277d609996ac';
SELECT retweet_user_id, retweet_tweet_id FROM tweets WHERE retweet_user_id is not null and retweet_user_id != '';


SELECT tweets_normal.user_id_str, source FROM tweets_normal where source like 'Twitter for BlackBerry®';

SELECT count(*) FROM (
                        SELECT count(*) as aa FROM tweets where tweet_language = 'en' group by user_id
                    ) as i;


SELECT * from tweets where retweet_user_id != '';

select user_id, count(*) as tweet_count from tweets where tweet_language = 'en' group by user_id;


SELECT * FROM tweets where r_user_created_at is not null;


SELECT user_id, count(*) as tweets_number FROM tweets WHERE user_id = '274d180d1de8828a8e3e7f62eec224ba9e3d04481e5d9eb29bf1cab882004a1b' GROUP BY user_id;

SELECT account_creation_date, user_profile_description, follower_count, following_count, user_reported_location, account_language,
       count_result.r_user_statuses_count, t.user_id
FROM tweets t
INNER JOIN (SELECT user_id, count(*) as r_user_statuses_count FROM tweets GROUP BY user_id) count_result ON count_result.user_id = t.user_id
WHERE t.user_id = '274d180d1de8828a8e3e7f62eec224ba9e3d04481e5d9eb29bf1cab882004a1b'
GROUP BY account_creation_date, user_profile_description, follower_count, following_count, user_reported_location, account_language,
       count_result.r_user_statuses_count, t.user_id;



SELECT r_user_followers_count, r_user_friends_count FROM tweets WHERE r_user_followers_count is not null;

SELECT count(*) FROM tweets_normal WHERE r_user_followers_count is not null;



select * from tweets where is_retweet is false;


select user_id, tweet_client_name, max(count) from
(select user_id, tweet_client_name, count(*) as count from tweets group by user_id, tweet_client_name) as i
group by user_id, tweet_client_name;


SELECT a.user_id, a.count, a.tweet_client_name
FROM (select user_id, tweet_client_name, count(*) as count from tweets group by user_id, tweet_client_name) as a
INNER JOIN (
    SELECT user_id, MAX(count) count
    FROM (select user_id, count(*) as count from tweets group by user_id, tweet_client_name) as aa
    GROUP BY user_id
) b ON a.user_id = b.user_id AND a.count = b.count
WHERE a.user_id = 'b6c1eb2e6a0d47539cc8d12e012c90c9e490e566977e7a27c1b5d2a3654b64d2';



SELECT user_id, tweet_client_name, count(*) as count
FROM tweets
WHERE user_id = 'b6c1eb2e6a0d47539cc8d12e012c90c9e490e566977e7a27c1b5d2a3654b64d2'
GROUP BY user_id, tweet_client_name
order by user_id;

SELECT t1.user_id, count(*) as cc FROM (
SELECT a.user_id, a.count, a.tweet_client_name
FROM (select user_id, tweet_client_name, count(*) as count from tweets where tweet_language ='en' group by user_id, tweet_client_name) as a
INNER JOIN (
    SELECT user_id, MAX(count) count
    FROM (select user_id, count(*) as count from tweets where tweet_language ='en' group by user_id, tweet_client_name) as aa
    GROUP BY user_id
) b ON a.user_id = b.user_id AND a.count = b.count) as t1
group by t1.user_id
order by cc desc;


select user_id from tweets group by user_id;

SELECT a.user_id_str, a.source, a.count
FROM (select user_id_str, source, count(*) as count from tweets_normal group by user_id_str, source) as a
INNER JOIN (
    SELECT user_id_str, MAX(count) count
    FROM (select user_id_str, count(*) as count from tweets_normal group by user_id_str, source) as aa
    GROUP BY user_id_str
) b ON a.user_id_str = b.user_id_str AND a.count = b.count;


select tweet_id, tweets.tweet_time, count(*) as ct from tweets group by tweets.tweet_time, tweet_id
order by ct desc;
select user_id, tweet_id, tweets.tweet_time, count(*) as ct from tweets group by tweets.tweet_time, user_id, tweet_id
order by ct desc;

SELECT sum(t1.ct) from (
                  select id_str, created_at, count(*) as ct
                  from tweets_normal
                  group by created_at, id_str
                  order by ct desc
) as t1
where t1.ct > 1;

SELECT DISTINCT count(*) FROM tweets_normal;

select count(*) from tweets where retweet_user_id = 'd6f0615523c7ebcb729e00d102921946754680ab141051dfc1ad93554ee44bb9' and is_retweet is true;

select count(*) from tweets where user_id = 'd6f0615523c7ebcb729e00d102921946754680ab141051dfc1ad93554ee44bb9' and is_retweet is true;

SELECT user_id, retweet_user_id, count(*) as number FROM tweets WHERE retweet_user_id != '' and retweet_user_id is not null GROUP BY user_id, retweet_user_id order by number desc;

select * from tweets_normal;

SELECT count(*) FROM
(SELECT user_id, retweet_user_id, count(*) as retweets_number FROM tweets WHERE retweet_user_id != '' and retweet_user_id is not null GROUP BY user_id, retweet_user_id) as t
WHERE retweets_number > 5;



SELECT user_id, retweet_user_id FROM (SELECT user_id, retweet_user_id, count(*) as retweets_number FROM tweets WHERE retweet_user_id != '' and retweet_user_id is not null GROUP BY user_id, retweet_user_id) as t
WHERE t.retweets_number > 2
GROUP BY user_id, retweet_user_id;



SELECT count(*) FROM (SELECT user_id_str, r_user_id_str, count(*) as retweets_number FROM tweets_normal WHERE r_user_id_str != '' and r_user_id_str is not null GROUP BY user_id_str, r_user_id_str) as t
WHERE retweets_number > 2 and user_id_str != r_user_id_str;


-- ----



SELECT (MAX(ratio)) as Ratio_, user_id_str
FROM
     (SELECT user_id_str, CAST(user_followers_count AS float) / CAST(user_friends_count + 1 AS float) as Ratio
     FROM tweets_n
     GROUP BY user_id_str, user_description, user_followers_count, user_friends_count) as tt
GROUP BY user_id_str;


SELECT CAST(follower_count AS float) / CAST(following_count + 1 AS float) as Ratio, user_id
FROM tweets
GROUP BY user_id, follower_count, following_count;



select id_str, text from tweets_n ORDER BY CHAR_LENGTH(text);

select tweet_text from tweets where tweet_id = '819816059100418048';




select user_id, max(follower_count) as follower, max(following_count) as following from tweets group by user_id;

select user_id_str, max(user_followers_count) as follower, max(user_friends_count) as following from tweets_n group by user_id_str;


select tweet_id, like_count from tweets;
select id_str, favorite_count from tweets_n;


SELECT lang, count(*) as count
from tweets_n
group by lang
order by count desc;


-- 292525    697230
select count(*) from tweets where is_retweet is true and r_user_followers_count is null



select count(*) from
(select distinct user_id_str from tweets_n) as tt;

select * from tweets_n where r_id_str is not null;

select * from tweets_n where q_id_str is not null;

select count(*) from tweets where quoted_tweet_tweet_id != '' and is_retweet is true

select count(*) from tweets where is_retweet is true and tweet_language = 'en';

select count(*) from (
                  select user_id, count(*) as counter from tweets where is_retweet is true group by user_id
)as tt

select distinct user_id from tweets where tweet_language = 'en';


select count(*) from tweets_n where r_id_str is not null;

select user_id_str, counter from (
                  select user_id_str, count(*) as counter from tweets_n where r_id_str is not null group by user_id_str
)as tt
where counter = 1

select count(*) from
(select distinct user_id_str from tweets_n) as tt;




select count(*) from tweets where tweet_language = 'en' and user_id = 'df5f61c2e94eda746801bb8738512b5c70da277f0e18533043b9f2e610c5748e';
select count(*) from tweets where user_id = 'df5f61c2e94eda746801bb8738512b5c70da277f0e18533043b9f2e610c5748e';



select  distinct t.user_id
from tweets t
inner join (select count(*) as count, user_id from tweets where tweet_language = 'en' group by user_id) as en_
on en_.user_id = t.user_id
inner join (select count(*) as count, user_id from tweets group by user_id) as all_
on all_.user_id = t.user_id
where en_.count = all_.count;


select distinct user_id from tweets where tweet_language = 'en'


select user_id_str
from
(select distinct user_id_str from tweets_n where user_verified is true and lang = 'en') as t

select * from tweets_n where user_id_str = '743238494399533056'


select distinct user_id_str from tweets_n where lang = 'en';

select count(*) as cnt, user_id from tweets group by user_id order by cnt



SELECT user_id, days_active::float8 / tweets_number::float8 as tweeting_frequency
FROM
     (SELECT user_id, account_creation_date, count(*) as tweets_number, date(max(tweet_time)) - account_creation_date as days_active
     FROM tweets GROUP BY user_id, account_creation_date
    ) as i

-- 51 sec 310ms
select * from tweets_n where user_id_str in ('207986661', '740721407361875969');

select user_id_str from tweets_n

SELECT user_id_str, max(user_followers_count) as user_followers_count, max(user_friends_count) as user_friends_count
FROM tweets_n GROUP BY user_id_str
limit 10;

select count(*) from tweets where tweet_language = 'en' and hashtags_count > 0


select text, hashtags from tweets_n where hashtags_count > 0;

select tweet_text, hashtags from tweets where hashtags_count > 0;

select tweet_text from tweets where tweet_text like '#';

select urls, tweet_text from tweets where urls_count > 0;

select count(*) from tweets_n where lang = 'en';

select text, id_str from tweets_n where id_str = '777680423845408768' or id_str = '777680423853981696'


select count(*) from
(select user_id_str from tweets_n where user_friends_count > 0 group by user_id_str) as isdas



SELECT user_id_str, count(*) as tweets_number
FROM tweets_n
GROUP BY user_id_str;


select tweet_text from tweets where tweet_id = '875297530636103686'

select urls from tweets_n where urls like '%ln.is%';


select * from tweets where tweet_language = 'en' and user_id = 'ca227621179b994c513cedaaf775cccf7462557becc0724e934bae124625a75d'

select count(*) from tweets_n where lang = 'en'

-- okolo 36%
select count(*) from tweets where tweet_language = 'en' and is_retweet = true;

select count(*) from tweets_n where lang = 'en' and r_text is not null;


select text, r_text from tweets_n where r_retweet_count is not null

select tweet_text from tweets where is_retweet is true


select * from tweets_n where id_str in ('789838798599356416', '789830781854224386');

select count(*) from tweets_n where user_id_str = '2706281318';
select source, created_at, text, id_str, user_description from tweets_n where user_id_str = '762685890963574784';

select count(*) from tweets_n where user_id_str = '771143268872572928';

select tweet_text from tweets where tweet_text like 'RT%';


select *
from (
         SELECT retweet_user_id,
                r_user_description,
                r_user_followers_count,
                r_user_friends_count,
                CAST(r_user_followers_count AS float) / CAST(r_user_friends_count + 1 AS float) as Ratio
         FROM tweets
         WHERE r_user_followers_count is not null
         GROUP BY retweet_user_id, r_user_description, r_user_followers_count, r_user_friends_count
) as t
where Ratio > 1 and Ratio < 2;

select distinct r_user_id_str, r_user_description
from (
         SELECT r_user_id_str,
                r_user_description,
                r_user_followers_count,
                r_user_friends_count,
                CAST(r_user_followers_count AS float) / CAST(r_user_friends_count + 1 AS float) as Ratio
         FROM tweets_n
         GROUP BY r_user_id_str, r_user_description, r_user_followers_count, r_user_friends_count
) as t
where Ratio > 1000000 and Ratio < 2000000;

select count(*) from tweets_n where r_user_id_str = '25073877';

select r_user_id_str, r_user_description from tweets_n where r_user_followers_count > 1500000;

select count(*) from
(select distinct user_id_str from tweets_n where lang = 'en' and r_user_followers_count is not null) as t

select count(*) from tweets_n where lang = 'en' and r_user_followers_count is not null;


select count(*) from
(select user_id_str, count(*) as cc from tweets_n where r_user_followers_count is not null group by user_id_str) as t
where cc = 1;


select * from tweets where tweet_id = '510079478156910592';

select * from tweets_n where id_str = '778667654806642688';