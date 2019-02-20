from lib.mysql_connect import connect
import spacy

MAX_WORD_LEN = 50

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
       )
       UNION
       (
         SELECT subreddit_id, CONCAT(title, ' ', self_text) AS body
         FROM links
       )
     ) AS links_and_comments_body
LIMIT 200
"""
cursor.execute(read_query)

number_of_links_comments = 0
words = {}

for (subredit_id, body) in cursor:

    if body is not None:
        subreddit = subredit_id.decode()
        if subreddit not in words:
            words[subreddit] = {}

        doc = nlp(body.decode())
        for token in doc:
            word = token.text.lower()
            if token.is_alpha and not token.is_stop and len(word) <= MAX_WORD_LEN:
                if word not in words[subreddit]:
                    words[subreddit][word] = 0
                words[subreddit][word] += 1


    number_of_links_comments += 1
    if number_of_links_comments % 100 == 0:
        print("Processed: {}".format(number_of_links_comments))


sql_insert_link = "INSERT INTO links_frequency_of_words (subreddit_id, word, frequency) VALUES (%s, %s, %s)"
for (subreddit, word_list) in words.items():
    for (word, frequency) in word_list.items():
        val = (
            subreddit,
            word,
            frequency
        )
        try:
            cursor.execute(sql_insert_link, val)
            conn.commit()
        except mysql.connector.IntegrityError as err:
            print("Insert error {}".format(err))


cursor.close()
