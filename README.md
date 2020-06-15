# Incels 2019

This repository is linked to the following papers: 

[1] Farrell, Tracie; Fernandez, Miriam; Novotny, Jakub and Alani, Harith (2019). Exploring Misogyny across the Manosphere in Reddit. In: WebSci '19 Proceedings of the 10th ACM Conference on Web Science, pp. 87–96.
http://oro.open.ac.uk/61128/1/WebScience139.pdf

[2] Farrell, Tracie; Araque, Oscar; Fernandez, Miriam and Alani, Harith (2020). On the use of Jargon and Word Embeddings to Explore Subculture within the Reddit’s Manosphere. In: WebSci'20 Proceedings of the 11th ACM Conference on Web Science.
http://oro.open.ac.uk/70529/1/WebSci2020%20%281%29.pdf

If you use the provided lexicon please reference [1] and if you use the provided annotated jargon, please reference [2], thx! :)


This README describes the steps to install and run various parts of this project

## Installation

### Python3 and Pip

This project requires Python version 3 and the respective Pip.

```bash
brew install python3 pip3
```

### Project dependencies

```bash
pip3 install -r requirements.txt

npm install -g electron@1.8.4 orca
```

### English language support

```
python3 -m spacy download en
```

## Running the scripts

### Database migration

Make sure all the SQL files from `database_migrations` folder have been run in the given order.



### Running the analysis

1. Frequency of authors per link for each subreddit:

`CalculateAuthorFrequency.sql`

2. Frequency of comments per link for each subreddit:

`CalculateCommentsFrequency.sql`

3. Frequency of words for each subreddit:

`CalculateWordsFrequency.py`

4. Identify if a word is in a dictionary and unique of a subreddit:

`CalculateWordsFlags.py`

5. Identify if a word is a reddit username:

`CalculateIsUserOnWordsFrequency.sql`

6. Frequency of ngrams for each subreddit:

`CalculateNgramsFrequency.py`

7. Annotate misogyny categories on links and comments:

`AnnotateCategoriesOnLinksAndComments.py`

8. Calculate monthly statistics of category frequency per subreddit

`CalculateMontlyStastistics.sql`

9. Calculate weekly statistics of category frequency per subreddit

`CalculateWeeklyStastistics.sql`

10. Calculate weekly statistics of word frequency per subreddit

`CalculateWordsWeeklyStatistics.py`

11. Calculate weekly statistics of author frequency per subreddit

`CalculateAuthorsWeeklyStatistics.sql`


### Visualising the results

1. Plot all categories of misogyny within and across subreddits 

`PlotCategoryEvolution.py`

2. Plot evolution of words within a category and a subreddit

`PlotCategoryWordsEvolutionAccrossCommunities.py`

3. Plot top authors per subreddit

`PlotTopAuthorsPerCommunity.py`

4. Plot authors across subreddits

`PlotAuthorsEvolutionAccrossCommunities.py`

5. Plot evolution of a word across subreddits

`PlotWordEvolutionAccrossCommunities.py`
