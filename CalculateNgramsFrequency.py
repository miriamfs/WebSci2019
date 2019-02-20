from lib.mysql_connect import connect
import spacy

MAX_WORD_LEN = 50
NGRAM_SIZE = 3

SUBREDIT_ID = ''

conn = connect()
cursor = conn.cursor()

nlp = spacy.load('en_core_web_sm')

read_query = """
SELECT subreddit_id, body
FROM (
       (
         SELECT links.subreddit_id, comments.body
         FROM links
                JOIN comments ON comments.auto_link_id = links.auto_id
         WHERE links.subreddit_id = '%s'
       )
       UNION
       (
         SELECT subreddit_id, CONCAT(title, ' ', self_text) AS body
         FROM links
         WHERE subreddit_id = '%s'
       )
     ) AS links_and_comments_body
""" % (SUBREDIT_ID, SUBREDIT_ID)
cursor.execute(read_query)

number_of_links_comments = 0
words = {}

for (subredit_id, body) in cursor:

    if body is not None:
        subreddit = subredit_id.decode()
        if subreddit not in words:
            words[subreddit] = {}

        doc = nlp(body.decode())
        for sentence in doc.sents:
            sentence_words = []
            for i in range(sentence.start, sentence.end):
                token = doc[i]
                word = token.text.lower()
                if not token.is_punct and not token.is_space and len(word) <= MAX_WORD_LEN:
                    sentence_words.append(word)

            if len(sentence_words) >= NGRAM_SIZE:
                for i in range(0, len(sentence_words) - NGRAM_SIZE + 1):
                    word = " ".join(sentence_words[i:(i + NGRAM_SIZE)])
                    if word not in words[subreddit]:
                        words[subreddit][word] = 0
                    words[subreddit][word] += 1


    number_of_links_comments += 1
    if number_of_links_comments % 100 == 0:
        print("Processed: {}".format(number_of_links_comments))

sql_insert_link = "" \
                  "INSERT INTO links_frequency_of_ngrams " \
                  "(subreddit_id, ngram, word_1, word_2, word_3, frequency) " \
                  "VALUES (%s, %s, %s, %s, %s, %s) " \
                  "ON DUPLICATE KEY UPDATE frequency = frequency + %s"
for (subreddit, ngram_list) in words.items():
    for (ngram, frequency) in ngram_list.items():
        words = ngram.split(" ")
        val = (
            subreddit,
            ngram,
            words[0],
            words[1],
            words[2],
            frequency,
            frequency
        )
        try:
            cursor.execute(sql_insert_link, val)
            conn.commit()
        except mysql.connector.IntegrityError as err:
            print("Insert error {}".format(err))


cursor.close()
