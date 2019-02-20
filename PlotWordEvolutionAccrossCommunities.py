from lib.mysql_connect import connect
from lib.constants import SUBREDDITS
from lib.constants import IMAGES_CONFIG
import plotly as py
import plotly.graph_objs as go
import plotly.io as pio
import os

conn = connect()
cursor = conn.cursor(buffered=True)

WORDS = []

if len(WORDS) == 0:
    print("Please provide at least one word in the WORDS constant above")
    exit()

PLOT_IMAGES = True

#
# Evolution of word graph
#
directory = "graphs/evolution_of_word_accross_communities"
if not os.path.exists(directory):
    os.makedirs(directory)

values = {}
for subreddit_id in SUBREDDITS.keys():
    values[subreddit_id] = {}

words_condition = '", "'.join(WORDS)
sql_select_words = """
SELECT subreddit_id, year_with_week, SUM(l_total) + SUM(c_total) AS total
FROM (
      (
        SELECT subreddit_id,
               DATE_FORMAT(created_utc, '%x-%v') AS year_with_week,
               COUNT(*)                          AS l_total,
               0                                 AS c_total
        FROM links
        WHERE MATCH(title, self_text) AGAINST('"{}"')
        GROUP BY subreddit_id, DATE_FORMAT(created_utc, '%x-%v')
        ORDER BY DATE_FORMAT(created_utc, '%x-%v')
      )
      UNION
      (
        SELECT links.subreddit_id,
               DATE_FORMAT(comments.created_utc, '%x-%v') AS year_with_week,
               0                                           AS l_total,
               COUNT(*)                                    AS c_total
        FROM comments
               JOIN links ON comments.auto_link_id = links.auto_id
        WHERE MATCH(body) AGAINST('"{}"')
        GROUP BY subreddit_id, DATE_FORMAT(comments.created_utc, '%x-%v')
        ORDER BY DATE_FORMAT(comments.created_utc, '%x-%v')
      )
    ) AS stats_from_links_and_comments
GROUP BY subreddit_id, year_with_week
ORDER BY year_with_week ASC
""".format(words_condition, words_condition)
cursor.execute(sql_select_words)

year_with_weeks = []

for (subreddit_id, year_with_week, total) in cursor:
    values[subreddit_id.decode()][year_with_week] = total

    if year_with_week not in year_with_weeks:
        year_with_weeks.append(year_with_week)

graph_data = []

for (subreddit_id, subreddit_name) in SUBREDDITS.items():
    y = []

    for year_with_week in year_with_weeks:
        if year_with_week in values[subreddit_id]:
            y.append(values[subreddit_id][year_with_week])
        else:
            y.append(0)

    trace = go.Scatter(
        x=year_with_weeks,
        y=y,
        mode='lines',
        name=subreddit_name
    )
    graph_data.append(trace)

if len(WORDS) == 1:
    graph_title = 'Word {}'.format(WORDS[0])
else:
    graph_title = 'Words {}'.format(', '.join(WORDS))


# Edit the layout
layout = dict(title=graph_title,
              xaxis=dict(
                  title='Year & Week',
                  type='category'
              ),
              yaxis=dict(title='Number of posts'),
              legend=IMAGES_CONFIG['legend']
              )

fig = dict(data=graph_data, layout=layout)
html_filename = '{}/word_{}.html'.format(directory, '+'.join(WORDS))
py.offline.plot(fig, filename=html_filename, image_width=1280, image_height=1024, auto_open=False)
if PLOT_IMAGES:
    png_filename = '{}/word_{}.png'.format(directory, '+'.join(WORDS))
    pio.write_image(fig, png_filename, **IMAGES_CONFIG['dimensions'])

conn.close()
