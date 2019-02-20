CREATE TABLE weekly_statistics
(
 subreddit_id VARCHAR(20) NOT NULL,
 year_with_week VARCHAR(10) NOT NULL,
 l_total INT NOT NULL,
 c_total INT NOT NULL,
 l_c_1 INT NOT NULL,
 c_c_1 INT NOT NULL,
 l_c_2 INT NOT NULL,
 c_c_2 INT NOT NULL,
 l_c_3 INT NOT NULL,
 c_c_3 INT NOT NULL,
 l_c_4 INT NOT NULL,
 c_c_4 INT NOT NULL,
 l_c_5 INT NOT NULL,
 c_c_5 INT NOT NULL,
 l_c_6 INT NOT NULL,
 c_c_6 INT NOT NULL,
 l_c_7 INT NOT NULL,
 c_c_7 INT NOT NULL,
 l_c_8 INT NOT NULL,
 c_c_8 INT NOT NULL,
 l_c_9 INT NOT NULL,
 c_c_9 INT NOT NULL,
 PRIMARY KEY (subreddit_id, year_with_week)
) COLLATE =utf8mb4_bin;