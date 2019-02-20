from lib.mysql_connect import connect
from lib.constants import SUBREDDITS
from lib.constants import IMAGES_CONFIG
import plotly as py
import plotly.graph_objs as go
import plotly.io as pio

import os

PLOT_IMAGES = True

conn = connect()
cursor = conn.cursor(buffered=True)

# Collect all year with months
year_with_weeks = []

sql_select_year_with_week = """
SELECT DISTINCT year_with_week
FROM authors_weekly_statistics
ORDER BY year_with_week
"""
cursor.execute(sql_select_year_with_week)
for (year_with_week,) in cursor:
    year_with_weeks.append(year_with_week.decode())

#
# Evolution of categories words in communities graph
#
directory = "graphs/evolution_of_authors_across_communities"
if not os.path.exists(directory):
    os.makedirs(directory)

graph_data = []

for (subreddit_id, subreddit_name) in SUBREDDITS.items():
    values = {}

    sql_select_words = """
    SELECT year_with_week, COUNT(*) AS author_count
    FROM authors_weekly_statistics
    WHERE subreddit_id LIKE '{}'
    GROUP BY year_with_week 
    ORDER BY year_with_week
    """.format(subreddit_id)
    cursor.execute(sql_select_words)
    for (year_with_week, author_count) in cursor:
        values[year_with_week.decode()] = author_count

    y = []
    for year_with_week in year_with_weeks:
        if year_with_week in values:
            y.append(values[year_with_week])
        else:
            y.append(0)

    trace = go.Scatter(
        x=year_with_weeks,
        y=y,
        mode='lines',
        name=subreddit_name
    )
    graph_data.append(trace)

# Edit the layout
layout = dict(title='Authors in Communities',
              xaxis=dict(
                  title='Year & Week',
                  type='category'
              ),
              yaxis=dict(title='Number of authors'),
              legend=IMAGES_CONFIG['legend']
              )

fig = dict(data=graph_data, layout=layout)
html_filename = '{}/authors.html'.format(directory)
png_filename = '{}/authors.png'.format(directory)
py.offline.plot(fig, filename=html_filename,image_width=1280,image_height=1024,auto_open=False)
if PLOT_IMAGES:
    pio.write_image(fig, png_filename, **IMAGES_CONFIG['dimensions'])


conn.close()
