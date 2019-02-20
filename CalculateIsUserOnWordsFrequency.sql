UPDATE links_frequency_of_words
SET is_user = 1
WHERE EXISTS
        (
          SELECT subreddit_id, author
          FROM (
                 (
                   SELECT subreddit_id, comments.author
                   FROM comments
                          JOIN links ON comments.auto_link_id = links.auto_id
                   GROUP BY subreddit_id, author
                 )
                 UNION
                 (
                   SELECT subreddit_id, author
                   FROM links
                   GROUP BY subreddit_id, author
                 )
               ) AS union_authors
          WHERE union_authors.subreddit_id = links_frequency_of_words.subreddit_id
            AND union_authors.author = links_frequency_of_words.word
        );