INSERT INTO authors_weekly_statistics
SELECT *
FROM (
       SELECT subreddit_id, author, year_with_week, SUM(l_total), SUM(c_total)
       FROM (
              (
                SELECT subreddit_id,
                       author,
                       DATE_FORMAT(created_utc, '%x-%v') AS year_with_week,
                       COUNT(*)                          AS l_total,
                       0                                 AS c_total
                FROM links
                GROUP BY subreddit_id, author, DATE_FORMAT(created_utc, '%x-%v')
                ORDER BY DATE_FORMAT(created_utc, '%x-%v')
              )
              UNION
              (
                SELECT links.subreddit_id,
                       comments.author,
                       DATE_FORMAT(comments.created_utc, '%x-%v') AS year_with_week,
                       0                                          AS l_total,
                       COUNT(*)                                   AS c_total
                FROM comments
                       JOIN links ON comments.auto_link_id = links.auto_id
                GROUP BY subreddit_id, comments.author, DATE_FORMAT(comments.created_utc, '%x-%v')
                ORDER BY DATE_FORMAT(comments.created_utc, '%x-%v')
              )
            ) AS stats_from_links_and_comments
       GROUP BY subreddit_id, author, year_with_week
     ) AS authors_weekly
