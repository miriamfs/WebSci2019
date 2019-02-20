from lib.mysql_connect import connect
from lib.constants import CATEGORY_WORDS

MAX_WORD_LEN = 50

conn = connect()
cursor = conn.cursor()

def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i+n]


CHUNK_SIZE = 100

TABLES = {
    'links': ['title', 'self_text'],
    'comments': ['body']
}

# Update all flags to false first to then avoid having to use WHERE condition for gaps
print("Setting all flags to FALSE as default")
for table in TABLES.keys():
    categories_columns = []
    for number in CATEGORY_WORDS.keys():
        categories_columns.append('is_category_{} = FALSE'.format(number))

    sql_update_flags = """
    UPDATE {}
    SET {};
    """.format(table, ', '.join(categories_columns))
    print(sql_update_flags)
    try:
        cursor.execute(sql_update_flags)
        conn.commit()
    except mysql.connector.IntegrityError as err:
        print("Update error {}".format(err))

for (category_id, words) in CATEGORY_WORDS.items():
    words_chunks = list(chunks(words, CHUNK_SIZE))
    for chunk in words_chunks:
        processed_words = []
        for word in chunk:
            processed_words.append('"{}"'.format(word.lower()))

        for (table, columns) in TABLES.items():
            match_query = """
            UPDATE {}
            SET is_category_{} = TRUE
            WHERE MATCH({}) AGAINST ('{}');
            """.format(table, category_id, ', '.join(columns), ' '.join(processed_words))
            print('Running the following query:')
            print(match_query)

            cursor.execute(match_query)
            conn.commit()

cursor.close()
