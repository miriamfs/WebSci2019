INSERT INTO links_frequency_of_comments
SELECT subreddit_id, number_of_comments, COUNT(*) AS frequency
FROM (
       SELECT links.subreddit_id, links.auto_id, IFNULL(number_of_comments, 0) AS number_of_comments
       FROM links
              LEFT JOIN (
         SELECT auto_link_id, COUNT(*) AS number_of_comments
         FROM comments
         GROUP BY auto_link_id
       ) AS comments_count ON links.auto_id = comments_count.auto_link_id
     ) AS processed_comments_count
GROUP BY subreddit_id, number_of_comments;
