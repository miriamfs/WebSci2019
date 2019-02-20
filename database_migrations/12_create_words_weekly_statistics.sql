CREATE TABLE words_weekly_statistics
(
  subreddit_id   VARCHAR(20) NOT NULL,
  word           VARCHAR(50) NOT NULL,
  year_with_week VARCHAR(10) NOT NULL,
  l_total        INT         NOT NULL,
  c_total        INT         NOT NULL,
  PRIMARY KEY (subreddit_id, word, year_with_week)
) COLLATE = utf8mb4_bin;

CREATE INDEX words_weekly_statistics_word_index
  ON words_weekly_statistics (word);

CREATE INDEX words_weekly_statistics_year_with_week_index
  ON words_weekly_statistics (year_with_week);
