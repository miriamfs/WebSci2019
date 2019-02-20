CREATE TABLE authors_weekly_statistics
(
  subreddit_id   VARCHAR(20) NOT NULL,
  author           VARCHAR(50) NOT NULL,
  year_with_week VARCHAR(10) NOT NULL,
  l_total        INT         NOT NULL,
  c_total        INT         NOT NULL,
  PRIMARY KEY (subreddit_id, author, year_with_week)
) COLLATE = utf8mb4_bin;

CREATE INDEX author_index
  ON authors_weekly_statistics (author);

CREATE INDEX year_with_week_index
  ON authors_weekly_statistics (year_with_week);
