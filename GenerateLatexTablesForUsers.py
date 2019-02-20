from lib.mysql_connect import connect
from lib.constants import SUBREDDITS
from lib.constants import CATEGORY_NAMES

conn = connect()
cursor = conn.cursor()

communities = {}

print("Querying totals")
community_totals_query = """
SELECT subreddit_id, SUM(total) AS total
FROM (
       (
         SELECT subreddit_id, COUNT(DISTINCT author) AS total
         FROM links
         GROUP BY subreddit_id
       )
       UNION
       (
         SELECT subreddit_id, COUNT(DISTINCT comments.author) AS total
         FROM comments
                JOIN links
                     ON links.auto_id = comments.auto_link_id
         GROUP BY subreddit_id
       )
     ) AS links_plus_comments
GROUP BY subreddit_id
"""
cursor.execute(community_totals_query)
for (subreddit_id, total) in cursor:
    communities[subreddit_id.decode()] = { 'total': int(total) }

print("Querying summary")
community_totals_query = """
SELECT subreddit_id, COUNT(DISTINCT author) AS total
FROM (
       (
         SELECT subreddit_id, author
         FROM links
         WHERE (
         is_category_1 = TRUE OR 
         is_category_2 = TRUE OR 
         is_category_3 = TRUE OR 
         is_category_4 = TRUE OR 
         is_category_5 = TRUE OR 
         is_category_6 = TRUE OR 
         is_category_7 = TRUE OR 
         is_category_8 = TRUE OR 
         is_category_9 = TRUE 
         )
         GROUP BY subreddit_id, author
       )
       UNION
       (
         SELECT subreddit_id, comments.author AS author
         FROM comments
                JOIN links
                     ON links.auto_id = comments.auto_link_id
         WHERE (
         comments.is_category_1 = TRUE OR 
         comments.is_category_2 = TRUE OR 
         comments.is_category_3 = TRUE OR 
         comments.is_category_4 = TRUE OR 
         comments.is_category_5 = TRUE OR 
         comments.is_category_6 = TRUE OR 
         comments.is_category_7 = TRUE OR 
         comments.is_category_8 = TRUE OR 
         comments.is_category_9 = TRUE 
         )            
         GROUP BY subreddit_id, comments.author
       )
     ) AS links_plus_comments
GROUP BY subreddit_id
"""
cursor.execute(community_totals_query)
for (subreddit_id, total) in cursor:
    communities[subreddit_id.decode()]['sum'] = int(total)


for (subreddit_id, total) in cursor:
    for category_id in CATEGORY_NAMES.keys():
        communities[subreddit_id.decode()][category_id] = 0


community_users_query = """
SELECT subreddit_id, COUNT(DISTINCT author) AS authors_count
FROM (
       (
         SELECT subreddit_id, author 
         FROM links
         WHERE is_category_{} = TRUE
         GROUP BY subreddit_id, author
       )
       UNION
       (
         SELECT subreddit_id, comments.author AS author
         FROM comments
                JOIN links ON links.auto_id = comments.auto_link_id
         WHERE comments.is_category_{} = TRUE
         GROUP BY subreddit_id, comments.author
       )
     ) AS authors_count_for_category
GROUP BY subreddit_id
"""

for (category_id, category_name) in CATEGORY_NAMES.items():
    print("Querying category {}".format(category_id))
    cursor.execute(community_users_query.format(category_id, category_id))
    for (subreddit_id, authors_count) in cursor:
        communities[subreddit_id.decode()][category_id] = int(authors_count)

print('--------------------------------------------------------')

for subreddit_id in communities.keys():
    line = []
    line.append(SUBREDDITS[subreddit_id])
    line.append(str(communities[subreddit_id]['total']))

    sum = communities[subreddit_id]['sum']
    line.append(str(sum))
    line.append(str(round(sum * 100 / communities[subreddit_id]['total'], 2)) + "%")

    for category_id in CATEGORY_NAMES.keys():
        num = communities[subreddit_id][category_id]
        line.append(str(num))
        line.append(str(round(num * 100 / communities[subreddit_id]['total'], 2)) + "%")

    print(' & '.join(line) + " \\\\ \\hline")

conn.close()
