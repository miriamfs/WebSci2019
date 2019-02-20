INSERT INTO links_frequency_of_authors
SELECT subreddit_id, number_of_authors, COUNT(*) AS frequency
FROM
(
  SELECT links.subreddit_id, links.auto_id, number_of_authors
  FROM links
         JOIN
       (
         SELECT auto_link_id, COUNT(*) AS number_of_authors
         FROM (
                SELECT DISTINCT auto_link_id, author
                FROM (
                       (
                         SELECT DISTINCT auto_link_id, author
                         FROM comments
                         GROUP BY auto_link_id, author
                       )
                       UNION
                       (
                         SELECT auto_id AS auto_link_id, author
                         FROM links
                       )
                     ) AS link_authors
              ) AS unique_link_authors
         GROUP BY auto_link_id
       ) AS link_authors_counts ON links.auto_id = link_authors_counts.auto_link_id
) AS processed_authors_count
GROUP BY subreddit_id, number_of_authors;
