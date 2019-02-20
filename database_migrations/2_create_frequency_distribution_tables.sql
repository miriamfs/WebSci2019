create table links_frequency_of_comments
(
	subreddit_id varchar(20) not null,
	num int not null,
	frequency int not null
);
create unique index links_frequency_of_comments_number_uindex
	on links_frequency_of_comments (subreddit_id, num);


create table links_frequency_of_authors
(
	subreddit_id varchar(20) not null,
	num int not null,
	frequency int not null
);
create unique index links_frequency_of_authors_number_uindex
	on links_frequency_of_authors (subreddit_id, num);
