from lib.mysql_connect import connect
from lib.constants import SUBREDDITS

conn = connect()
cursor = conn.cursor()

table_query = """
SELECT subreddit_id,
       total,
       (c_1 + c_2 + c_3 + c_4 + c_5 + c_6 + c_7 + c_8 + c_9)                         AS sum,
       ROUND((c_1 + c_2 + c_3 + c_4 + c_5 + c_6 + c_7 + c_8 + c_9) * 100 / total, 2) AS sum_p,
       c_1,
       ROUND(c_1 * 100 / total, 2)                                                   AS c_1_p,
       c_2,
       ROUND(c_2 * 100 / total, 2)                                                   AS c_2_p,
       c_3,
       ROUND(c_3 * 100 / total, 2)                                                   AS c_3_p,
       c_4,
       ROUND(c_4 * 100 / total, 2)                                                   AS c_4_p,
       c_5,
       ROUND(c_5 * 100 / total, 2)                                                   AS c_5_p,
       c_6,
       ROUND(c_6 * 100 / total, 2)                                                   AS c_6_p,
       c_7,
       ROUND(c_7 * 100 / total, 2)                                                   AS c_7_p,
       c_8,
       ROUND(c_8 * 100 / total, 2)                                                   AS c_8_p,
       c_9,
       ROUND(c_9 * 100 / total, 2)                                                   AS c_9_p
FROM (
       SELECT subreddit_id,
              SUM(l_total + c_total) AS total,
              SUM(l_c_1 + c_c_1)     AS c_1,
              SUM(l_c_2 + c_c_2)     AS c_2,
              SUM(l_c_3 + c_c_3)     AS c_3,
              SUM(l_c_4 + c_c_4)     AS c_4,
              SUM(l_c_5 + c_c_5)     AS c_5,
              SUM(l_c_6 + c_c_6)     AS c_6,
              SUM(l_c_7 + c_c_7)     AS c_7,
              SUM(l_c_8 + c_c_8)     AS c_8,
              SUM(l_c_9 + c_c_9)     AS c_9
       FROM weekly_statistics
       GROUP BY subreddit_id
     ) AS subreddit_summary
"""
rows = []
cursor.execute(table_query)
for row in cursor:
    line = []
    line.append(SUBREDDITS[row[0].decode()])
    line.append(str(row[1]))
    c = 0
    for column in row[2:]:
        if c % 2 == 1:
            line.append(str(column) + '%')
        else:
            line.append(str(column))
        c += 1

    print(' & '.join(line) + " \\\\ \\hline")

conn.close()
