import nfldb
from jinja2 import Template
import pandas as pd

db = nfldb.connect()


def top_5_rushers():
    q = nfldb.Query(db)
    q.game(season_year=2015, season_type='Regular')
    for pp in q.sort('rushing_yds').limit(5).as_aggregate():
        print pp.player, pp.rushing_yds


def passing_yds_by_week():
    for wk in range(1, 17):
        q_brady = nfldb.Query(db)
        q_brady.game(season_year=2015, season_type='Regular', week=wk)
        q_brady.player(full_name='Tom Brady')
        for pp in q_brady.as_aggregate():
            print pp.player, pp.passing_yds


def query_from_template():
    with open('sql/passing_yds_per_game.sql.j2') as f:
        template = Template(f.read())
    query = template.render(year=2015, full_name='Tom Brady')
    print query
    conn = 'postgres://nfldb:nfldb@localhost:5432/nfldb'
    results = pd.read_sql(query, conn)
    print results


if __name__ == '__main__':
    passing_yds_by_week()
    query_from_template()

