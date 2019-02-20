from lib.mysql_connect import connect

NUMBER_OF_EXAMPLES = 3

conn = connect()
cursor = conn.cursor()

words = {}

words_query = """
SELECT DISTINCT word, frequency
FROM links_frequency_of_words
WHERE is_unique = 1
  AND in_vocabulary = 0
  AND (is_user IS NULL OR is_user = FALSE)
  AND frequency > 10
ORDER BY frequency DESC
"""
cursor.execute(words_query)
for (word, frequency) in cursor:
    words[word] = frequency

for word in words.keys():
    top_comments_query = """
    SELECT body
    FROM ((SELECT body, MATCH(body) AGAINST('"{}"') AS score
       FROM comments
       WHERE MATCH(body) AGAINST('"{}"')
       ORDER BY MATCH(body) AGAINST('"{}"') DESC
       LIMIT {})
      UNION
      (SELECT CONCAT(title, ' ', self_text) AS body, MATCH(title, self_text) AGAINST('"{}"') AS score
       FROM links
       WHERE MATCH(title, self_text) AGAINST('"{}"')
       ORDER BY MATCH(title, self_text) AGAINST('"{}"') DESC
       LIMIT {})) AS matches
        ORDER BY score DESC
        LIMIT {}
    """.format(word, word, word, NUMBER_OF_EXAMPLES, word, word, word, NUMBER_OF_EXAMPLES, NUMBER_OF_EXAMPLES)
    cursor.execute(top_comments_query)

    examples = []
    for (body,) in cursor:
        if body is not None:
            examples.append(body.decode().replace("\n", " ").replace('"', "'"))

    if len(examples) == 3:
        for example in examples:
            print('"{}","{}","{}"'.format(word, words[word], example))


cursor.close()
