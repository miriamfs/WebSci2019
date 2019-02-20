INSERT INTO weekly_statistics
SELECT stats_links.subreddit_id, stats_links.year_with_week, l_total, c_total,
       l_c_1, c_c_1, l_c_2, c_c_2, l_c_3, c_c_3,
       l_c_4, c_c_4, l_c_5, c_c_5, l_c_6, c_c_6,
       l_c_7, c_c_7, l_c_8, c_c_8, l_c_9, c_c_9
FROM (
       SELECT subreddit_id,
              DATE_FORMAT(created_utc, '%x-%v') AS year_with_week,
              COUNT(*)                          AS l_total,
              SUM(is_category_1)                AS l_c_1,
              SUM(is_category_2)                AS l_c_2,
              SUM(is_category_3)                AS l_c_3,
              SUM(is_category_4)                AS l_c_4,
              SUM(is_category_5)                AS l_c_5,
              SUM(is_category_6)                AS l_c_6,
              SUM(is_category_7)                AS l_c_7,
              SUM(is_category_8)                AS l_c_8,
              SUM(is_category_9)                AS l_c_9
       FROM links
       GROUP BY subreddit_id, DATE_FORMAT(created_utc, '%x-%v')
       ORDER BY DATE_FORMAT(created_utc, '%x-%v')
     ) AS stats_links
       JOIN (
  SELECT subreddit_id,
         DATE_FORMAT(comments.created_utc, '%x-%v') AS year_with_week,
         COUNT(*)                                   AS c_total,
         SUM(comments.is_category_1)                AS c_c_1,
         SUM(comments.is_category_2)                AS c_c_2,
         SUM(comments.is_category_3)                AS c_c_3,
         SUM(comments.is_category_4)                AS c_c_4,
         SUM(comments.is_category_5)                AS c_c_5,
         SUM(comments.is_category_6)                AS c_c_6,
         SUM(comments.is_category_7)                AS c_c_7,
         SUM(comments.is_category_8)                AS c_c_8,
         SUM(comments.is_category_9)                AS c_c_9
  FROM comments
         JOIN links
              ON links.auto_id = comments.auto_link_id
  GROUP BY subreddit_id, DATE_FORMAT(comments.created_utc, '%x-%v')
  ORDER BY DATE_FORMAT(comments.created_utc, '%x-%v')) AS stats_comments
            ON stats_links.subreddit_id = stats_comments.subreddit_id AND
               stats_links.year_with_week = stats_comments.year_with_week;