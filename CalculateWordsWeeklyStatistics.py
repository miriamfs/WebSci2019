from lib.mysql_connect import connect
import mysql.connector
from lib.constants import CATEGORY_WORDS

CLEAN_TABLE_BEFORE_RUN = False

conn = connect()
cursor = conn.cursor()

if CLEAN_TABLE_BEFORE_RUN:
    print("Truncating words_weekly_statistics")
    truncate_query = "TRUNCATE words_weekly_statistics"
    cursor.execute(truncate_query)
    conn.commit()

unique_words = []
for (id,words) in CATEGORY_WORDS.items():
    for word in words:
        processed = word.lower()
        if processed not in unique_words:
            unique_words.append(processed)

word_query = """
INSERT INTO words_weekly_statistics
SELECT *
FROM (
       SELECT subreddit_id, '{}' AS word, year_with_week, SUM(l_total), SUM(c_total)
       FROM (
              (
                SELECT subreddit_id,
                       DATE_FORMAT(created_utc, '%x-%v') AS year_with_week,
                       COUNT(*)                          AS l_total,
                       0                                 AS c_total
                FROM links
                WHERE MATCH(title, self_text) AGAINST('"{}"')
                GROUP BY subreddit_id, DATE_FORMAT(created_utc, '%x-%v')
                ORDER BY DATE_FORMAT(created_utc, '%x-%v')
              )
              UNION
              (
                SELECT links.subreddit_id,
                       DATE_FORMAT(comments.created_utc, '%x-%v') AS year_with_week,
                       0                                           AS l_total,
                       COUNT(*)                                    AS c_total
                FROM comments
                       JOIN links ON comments.auto_link_id = links.auto_id
                WHERE MATCH(body) AGAINST('"{}"')
                GROUP BY subreddit_id, DATE_FORMAT(comments.created_utc, '%x-%v')
                ORDER BY DATE_FORMAT(comments.created_utc, '%x-%v')
              )
            ) AS stats_from_links_and_comments
       GROUP BY subreddit_id, year_with_week
     ) AS words_weekly
"""

for (word) in unique_words:
    print("- {}".format(word))

    query = word_query.format(word, word, word)
    try:
        cursor.execute(query)
        conn.commit()
    except mysql.connector.IntegrityError as err:
        print("Insert error {}".format(err))
        print(query)

cursor.close()
