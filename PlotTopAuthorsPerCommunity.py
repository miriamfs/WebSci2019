from lib.mysql_connect import connect
from lib.constants import SUBREDDITS
import plotly as py
import plotly.graph_objs as go
import os

NUMBER_OF_AUTHORS = 15

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
directory = "graphs/top_authors_per_community"
if not os.path.exists(directory):
    os.makedirs(directory)


for (subreddit_id, subreddit_name) in SUBREDDITS.items():
    values = {}

    sql_select_top_authors = """
    SELECT author, SUM(l_total + c_total) AS total
    FROM authors_weekly_statistics
    WHERE subreddit_id LIKE '{}'
    GROUP BY author
    ORDER BY total DESC
    LIMIT {}
    """.format(subreddit_id, NUMBER_OF_AUTHORS)
    cursor.execute(sql_select_top_authors)
    for (author, total) in cursor:
        values[author.decode()] = {}

    if len(values.keys()) > 0:
        sql_select_authors = """
        SELECT author, year_with_week, l_total + c_total AS total
        FROM authors_weekly_statistics
        WHERE subreddit_id LIKE '{}' AND 
              author IN ('{}')
        ORDER BY year_with_week
        """.format(subreddit_id, "', '".join(values.keys()))
        cursor.execute(sql_select_authors)
        for (author, year_with_week, total) in cursor:
            values[author.decode()][year_with_week.decode()] = total

        graph_data = []
        for author in values.keys():
            y = []

            for year_with_week in year_with_weeks:
                if year_with_week in values[author]:
                    y.append(values[author][year_with_week])
                else:
                    y.append(0)

            trace = go.Scatter(
                x=year_with_weeks,
                y=y,
                mode='lines',
                name=author
            )
            graph_data.append(trace)

        # Edit the layout
        layout = dict(title='Top Authors in Community {}'.format(subreddit_name),
                      xaxis=dict(
                          title='Year & Week',
                          type='category'
                      ),
                      yaxis=dict(title='Number of contributions'),
                      )

        fig = dict(data=graph_data, layout=layout)
        filename = '{}/community_{}.html'.format(directory, subreddit_name)
        py.offline.plot(fig, filename=filename, image_width=1280, image_height=1024, auto_open=False)

conn.close()
