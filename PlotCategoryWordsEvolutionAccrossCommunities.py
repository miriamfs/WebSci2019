from lib.mysql_connect import connect
from lib.constants import SUBREDDITS
from lib.constants import CATEGORY_NAMES
from lib.constants import CATEGORY_WORDS
from lib.constants import IMAGES_CONFIG
import plotly as py
import plotly.graph_objs as go
import plotly.io as pio
import os

conn = connect()
cursor = conn.cursor(buffered=True)

WORDS_FROM_EACH_CATEGORY = 15

PLOT_IMAGES = True

# Get highest frequency words for each category
category_words = {}

for (category_id, words) in CATEGORY_WORDS.items():
    category_words[category_id] = []

    sql_select_words = """
    SELECT word, SUM(l_total + c_total) AS score
    FROM words_weekly_statistics
    WHERE word IN ('{}')
    GROUP BY word
    ORDER BY score DESC
    LIMIT {}
    """.format("','".join(words), WORDS_FROM_EACH_CATEGORY)
    cursor.execute(sql_select_words)
    for (word,total) in cursor:
        category_words[category_id].append(word.decode())

# Collect all year with months
year_with_weeks = []

sql_select_year_with_week = """
SELECT DISTINCT year_with_week
FROM words_weekly_statistics
ORDER BY year_with_week
"""
cursor.execute(sql_select_year_with_week)
for (year_with_week,) in cursor:
    year_with_weeks.append(year_with_week.decode())

#
# Evolution of categories words in communities graph
#
directory = "graphs/evolution_of_category_words_accross_communities"
if not os.path.exists(directory):
    os.makedirs(directory)

for (subreddit_id, subreddit_name) in SUBREDDITS.items():
    for (category_id, category_name) in CATEGORY_NAMES.items():
        values = {}
        for word in category_words[category_id]:
            values[word] = {}

        sql_select_words = """
            SELECT word, year_with_week, (l_total + c_total) AS total
            FROM words_weekly_statistics
            WHERE 
                subreddit_id LIKE '{}' AND 
                word IN ('{}')
            ORDER BY year_with_week
            """.format(subreddit_id, "','".join(category_words[category_id]))
        cursor.execute(sql_select_words)
        for (word, year_with_week, total) in cursor:
            values[word.decode()][year_with_week.decode()] = total

        graph_data = []
        for word in category_words[category_id]:
            y = []
            for year_with_week in year_with_weeks:
                if year_with_week in values[word]:
                    y.append(values[word][year_with_week])
                else:
                    y.append(0)

            trace = go.Scatter(
                x=year_with_weeks,
                y=y,
                mode='lines',
                name=word
            )
            graph_data.append(trace)

        # Edit the layout
        layout = dict(title='Community {}, Category {}'.format(subreddit_name, category_name),
                      xaxis=dict(
                          title='Year & Week',
                          type='category'
                      ),
                      yaxis=dict(title='Number of posts'),
                      legend=IMAGES_CONFIG['legend']
                      )

        fig = dict(data=graph_data, layout=layout)
        html_filename = '{}/community_{}-category_{}.html'.format(directory, subreddit_name.replace(' ', '-'), category_name.replace(' ', '-'))
        py.offline.plot(fig, filename=html_filename, image_width=1280, image_height=1024, auto_open=False)
        if PLOT_IMAGES:
            png_filename = '{}/community_{}-category_{}.png'.format(directory, subreddit_name.replace(' ', '-'), category_name.replace(' ', '-'))
            pio.write_image(fig, png_filename, **IMAGES_CONFIG['dimensions'])

conn.close()
