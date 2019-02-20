create table links_frequency_of_words
(
	subreddit_id varchar(20) not null,
	word varchar(50) not null,
	frequency int not null
);
create unique index links_frequency_of_words_word_uindex
	on links_frequency_of_words (subreddit_id, word);
