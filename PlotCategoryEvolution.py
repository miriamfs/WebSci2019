from lib.mysql_connect import connect
from lib.constants import CATEGORY_NAMES
from lib.constants import SUBREDDITS
from lib.constants import IMAGES_CONFIG
import plotly as py
import plotly.graph_objs as go
import plotly.io as pio
import os

conn = connect()
cursor = conn.cursor(buffered=True)

PLOT_IMAGES = True

# Collect all year with months
year_with_weeks = []

sql_select_year_with_week = """
SELECT DISTINCT year_with_week
FROM weekly_statistics
ORDER BY year_with_week
"""
cursor.execute(sql_select_year_with_week)
for (year_with_week,) in cursor:
    year_with_weeks.append(year_with_week.decode())

#
# Evolution of categories graphs
#
directory = "graphs/evolution_of_categories"
if not os.path.exists(directory):
    os.makedirs(directory)

for category in CATEGORY_NAMES.keys():
    graph_data = []

    # Select values for all subreddits
    values = {}

    sql_select_category = """
    SELECT subreddit_id, year_with_week, l_total, c_total, l_c_{}, c_c_{}
    FROM weekly_statistics
    ORDER BY year_with_week
    """.format(category, category)
    cursor.execute(sql_select_category)
    for (subreddit_id_encoded, year_with_week_encoded, l_total, c_total, l_c, c_c) in cursor:
        subreddit_id = subreddit_id_encoded.decode()
        year_with_week = year_with_week_encoded.decode()

        if year_with_week not in values:
            values[year_with_week] = {}

        # values[year_with_week][subreddit_id] = round((l_c + c_c) * 100 / (l_total + c_total), 2)
        values[year_with_week][subreddit_id] = l_c + c_c

    for subreddit_id in SUBREDDITS.keys():
        y = []
        for year_with_week in year_with_weeks:
            if subreddit_id in values[year_with_week]:
                y.append(values[year_with_week][subreddit_id])
            else:
                y.append(0)

        trace = go.Scatter(
            x=year_with_weeks,
            y=y,
            mode='lines',
            name=SUBREDDITS[subreddit_id]
        )

        graph_data.append(trace)

    # Edit the layout
    layout = dict(title='Category {}'.format(CATEGORY_NAMES[category]),
                  xaxis=dict(
                      title='Year & Week',
                      type='category'
                  ),
                  yaxis=dict(title='Number of posts'),
                  legend=IMAGES_CONFIG['legend']
                  )

    fig = dict(data=graph_data, layout=layout)
    html_filename = '{}/category_{}.html'.format(directory, CATEGORY_NAMES[category].replace(' ', '-'))
    png_filename = '{}/category_{}.png'.format(directory, CATEGORY_NAMES[category].replace(' ', '-'))
    py.offline.plot(fig, filename=html_filename,image_width=1280,image_height=1024,auto_open=False)
    if PLOT_IMAGES:
        pio.write_image(fig, png_filename, **IMAGES_CONFIG['dimensions'])

#
# Evolution of communities graphs with and without totals
#
directory_with_totals = "graphs/evolution_of_communities_with_totals"
if not os.path.exists(directory_with_totals):
    os.makedirs(directory_with_totals)

directory_without_totals = "graphs/evolution_of_communities"
if not os.path.exists(directory_without_totals):
    os.makedirs(directory_without_totals)

for (subreddit_id,subreddit_name) in SUBREDDITS.items():
    first_week = None
    graph_data = []

    sql_select_subreddit = """
    SELECT year_with_week,
        (l_total + c_total),
        (l_c_1 + c_c_1),
        (l_c_2 + c_c_2), 
        (l_c_3 + c_c_3), 
        (l_c_4 + c_c_4), 
        (l_c_5 + c_c_5),  
        (l_c_6 + c_c_6),  
        (l_c_7 + c_c_7),  
        (l_c_8 + c_c_8),  
        (l_c_9 + c_c_9)  
    FROM weekly_statistics
    WHERE subreddit_id = '{}'
    ORDER BY year_with_week
    """.format(subreddit_id)
    cursor.execute(sql_select_subreddit)

    subreddit_weeks = {}
    total_weeks = {}
    for values in cursor:
        week = values[0].decode()
        if first_week is None:
            first_week = week

        total_weeks[week] = values[1]
        subreddit_weeks[week] = values[2:11]

    useful_weeks = [week for week in year_with_weeks if week >= first_week]

    for (id, name) in CATEGORY_NAMES.items():
        y = []
        for year_with_week in useful_weeks:
            if year_with_week in subreddit_weeks:
                y.append(subreddit_weeks[year_with_week][id - 1])
            else:
                y.append(0)

        trace = go.Scatter(
            x=useful_weeks,
            y=y,
            mode='lines',
            name=name
        )
        graph_data.append(trace)

    # Edit the layout
    layout = dict(title='Community {}'.format(subreddit_name),
                  xaxis=dict(
                      title='Year & Week',
                      type='category'
                  ),
                  yaxis=dict(title='Number of posts'),
                  legend=IMAGES_CONFIG['legend']
                  )

    fig = dict(data=graph_data, layout=layout)
    html_filename = '{}/community_{}.html'.format(directory_without_totals, subreddit_name.replace(' ', '-'))
    png_filename = '{}/community_{}.png'.format(directory_without_totals, subreddit_name.replace(' ', '-'))
    py.offline.plot(fig, filename=html_filename, image_width=1280, image_height=1024, auto_open=False)
    if PLOT_IMAGES:
        pio.write_image(fig, png_filename, **IMAGES_CONFIG['dimensions'])

    y = []
    for year_with_week in useful_weeks:
        if year_with_week in total_weeks:
            y.append(total_weeks[year_with_week])
        else:
            y.append(0)

    trace = go.Scatter(
        x=useful_weeks,
        y=y,
        mode='lines',
        name='Total'
    )
    graph_data.append(trace)

    # Edit the layout
    layout = dict(title='Community {}'.format(subreddit_name),
                  xaxis=dict(
                      title='Year & Week',
                      type='category'
                  ),
                  yaxis=dict(title='Number of posts'),
                  legend=IMAGES_CONFIG['legend']
                  )

    fig = dict(data=graph_data, layout=layout)
    filename = '{}/community_{}.html'.format(directory_with_totals, subreddit_name.replace(' ', '-'))
    py.offline.plot(fig, filename=filename,image_width=1280,image_height=1024,auto_open=False)

conn.close()
