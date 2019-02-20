from lib.mysql_connect import connect
from lib.constants import CATEGORY_NAMES
from lib.constants import CATEGORY_WORDS
import operator

conn = connect()
cursor = conn.cursor()

category_word_frequency = {}

word_query = """
SELECT SUM(num) AS total
FROM (
       (SELECT COUNT(*) AS num
        FROM comments
        WHERE MATCH(body) AGAINST('"{}"')
         )
         UNION
       (
         SELECT COUNT(*) AS num
         FROM links
         WHERE MATCH(title, self_text) AGAINST('"{}"')
       )
  ) AS word_count_in_comments_and_links

"""
for (category_id, words) in CATEGORY_WORDS.items():
    words_frequency = {}
    for word in words:
        cursor.execute(word_query.format(word, word))
        row = cursor.fetchone()
        if row[0] is not None:
            total = int(row[0])
            if total > 0:
                words_frequency[word] = int(row[0])

    category_word_frequency[category_id] = dict(sorted(words_frequency.items(), key=operator.itemgetter(1), reverse=True)[0:5])

print('---------------------------------------------------------------------')

line1 = []
line2 = []
for (category_id, category_name) in CATEGORY_NAMES.items():
    line1.append("\\multicolumn{2}{c|}{%s}" %(category_name))
    line2.append('word')
    line2.append('frequency')

print(' & '.join(line1))
print(' & '.join(line2))

for i in range(0, 5):
    line = []
    for category_id in CATEGORY_NAMES.keys():
        try:
            word = list(category_word_frequency[category_id].keys())[i]
            line.append(word)
            line.append(str(category_word_frequency[category_id][word]))
        except IndexError:
            line.append('-')
            line.append('-')

    print(' & '.join(line))



conn.close()
