CREATE FULLTEXT INDEX links_author_index
  ON links (author);

CREATE FULLTEXT INDEX comments_author_index
  ON comments (author);
