create table links_frequency_of_ngrams
(
	subreddit_id varchar(20) not null,
	ngram varchar(200) not null,
	word_1 varchar(50) not null,
	word_2 varchar(50) not null,
	word_3 varchar(50) not null,
	frequency int not null
);
create unique index links_frequency_of_ngrams_ngram_uindex
	on links_frequency_of_ngrams (subreddit_id, ngram);
