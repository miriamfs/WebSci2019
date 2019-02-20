from lib.mysql_connect import connect
import spacy

nlp = spacy.load('en_core_web_sm')

conn = connect()
cursor = conn.cursor(buffered=True)

# Update all flags to false first to then avoid having to use WHERE condition for gaps
print("Setting all flags to FALSE as default")
sql_update_flags = "UPDATE links_frequency_of_words SET in_vocabulary = FALSE, is_unique = FALSE, is_complete = FALSE"
try:
    cursor.execute(sql_update_flags)
    conn.commit()
except mysql.connector.IntegrityError as err:
    print("Update error {}".format(err))

subreddits_count = 0
words_in_dictionary = []
words_unique_complete = {}

sql_select_subreddit_count = "SELECT COUNT(DISTINCT subreddit_id) FROM links_frequency_of_words"
cursor.execute(sql_select_subreddit_count)
row = cursor.fetchone()
if row[0] is not None:
    subreddits_count = row[0]

sql_select_words_with_subreddits = """
SELECT word, GROUP_CONCAT(subreddit_id SEPARATOR '|')
FROM links_frequency_of_words
GROUP BY word
"""
cursor.execute(sql_select_words_with_subreddits)

for (word, subreddits_string) in cursor:
    # Calculate in_dictionary flag - per unique words across subreddits
    if word in nlp.vocab:
        words_in_dictionary.append(word)

    subreddits_list = subreddits_string.split('|')
    if len(subreddits_list) < subreddits_count:
        words_unique_complete[word] = subreddits_list


# Update in_vocabulary flags
print("Updating in_dictionary with words in dictionary: {}".format(len(words_in_dictionary)))
i = 0
sql_update_dictionary = "UPDATE links_frequency_of_words SET in_vocabulary = TRUE WHERE word = %s"
for word in words_in_dictionary:
    try:
        cursor.execute(sql_update_dictionary, (word,))
        conn.commit()
    except mysql.connector.IntegrityError as err:
        print("Update error {}".format(err))

    i += 1
    if i % 1000 == 0:
        print("- processed: {}".format(i))

# Update is_unique and is_complete
print("Updating is_unique, is_complete with distinct words: {}".format(len(words_unique_complete)))
i = 0
sql_update_unique_complete = """
UPDATE links_frequency_of_words 
SET is_unique = TRUE, is_complete = TRUE 
WHERE word = %s AND subreddit_id = %s
"""
sql_update_complete = """
UPDATE links_frequency_of_words 
SET is_complete = TRUE 
WHERE word = %s AND subreddit_id IN ({})
"""
for (word, subreddits_list) in words_unique_complete.items():
    try:
        if len(subreddits_list) == 1:
            cursor.execute(sql_update_unique_complete, (word, subreddits_list[0]))
        else:
            # This is a very stupid way of being able to use IN for Mysql efficiency
            format_strings = ','.join(['%s'] * len(subreddits_list))
            subreddits_list.insert(0, word) # this is to be able to put the word to the SQL interpolation
            cursor.execute(sql_update_complete.format(format_strings), subreddits_list)
            
        conn.commit()
    except mysql.connector.IntegrityError as err:
        print("Update error {}".format(err))

    i += 1
    if i % 1000 == 0:
        print("- processed: {}".format(i))

conn.close()
