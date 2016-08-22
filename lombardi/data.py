import nfldb
from jinja2 import Template
import pandas as pd

db = nfldb.connect()
conn = 'postgres://nfldb:nfldb@localhost:5432/nfldb'

map_metric_range = dict(
    passing_yds=600,
    rushing_yds=400,
    receiving_yds=400,
    passing_tds=8,
    rushing_tds=4,
    receiving_tds=4,
)

def metric_range(metric):
    return map_metric_range[metric]


def player_metric(player, metric, min_year=None, max_year=None):

    # retrieve data
    with open('sql/by_game_template.sql') as f:
        template = Template(f.read())

    query = template.render(
        player=player,
        metric=metric,
        min_year=min_year,
        max_year=max_year,
    )

    results = pd.read_sql(query,conn)
    return list(results[metric])



