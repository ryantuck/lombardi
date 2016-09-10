import nfldb
from jinja2 import Template
import pandas as pd

db = nfldb.connect()
read_conn = 'postgres://nfldb:nfldb@localhost:5432/nfldb'
write_conn = 'postgres://ryan:ryanryan@localhost:5432/lombardi'

map_metric_range = dict(
    passing_yds=600,
    rushing_yds=300,
    receiving_yds=300,
    passing_tds=8,
    rushing_tds=4,
    receiving_tds=4,
)

def metric_range(metric):
    return map_metric_range[metric]


def player_metric(player, metric, min_year=None, max_year=None):

    results = player_df(player, metric, min_year, max_year)
    return list(results[metric])


def player_df(player, metric, min_year=None, max_year=None):

    # retrieve data
    with open('sql/by_game_template.sql') as f:
        template = Template(f.read())

    query = template.render(
        player=player,
        metric=metric,
        min_year=min_year,
        max_year=max_year,
    )

    return pd.read_sql(query,read_conn).sort_values(by=['year', 'week'])


def active_rbs():

    with open('sql/rb_list.sql') as f:
        query = f.read()

    return pd.read_sql(query,read_conn)


def demo_players():
    return {
        'qb': {
            'players': [
                'Tom Brady',
                'Cam Newton',
                'Aaron Rodgers',
                'Russell Wilson',
                'Drew Brees',
                'Matt Ryan',
                'Andrew Luck',
                'Eli Manning',
                'Ryan Tannehill',
                'Jay Cutler',
                'Matthew Stafford',
                'Joe Flacco'
            ],
            'metric': 'passing_yds',
        },
        'rb': {
            'players': [
                'Jamaal Charles',
                'Adrian Peterson',
                'LeSean McCoy',
                'Eddie Lacy',
                'LeGarrette Blount',
                'C.J. Anderson',
                'Matt Forte',
                'Mark Ingram',
                'DeMarco Murray',
                'Frank Gore',
                'Darren Sproles',
                'Todd Gurley',
            ],
            'metric': 'rushing_yds',
        },
        'wr': {
            'players': [
                'Antonio Brown',
                'Odell Beckham',
                'Julio Jones',
                'DeAndre Hopkins',
                'A.J. Green',
                'Dez Bryant',
                'Jordy Nelson',
                'Mike Evans',
                'Alshon Jeffery',
                'T.Y. Hilton',
                'Randall Cobb',
                'Demaryius Thomas'
            ],
            'metric': 'receiving_yds'
        }
    }
