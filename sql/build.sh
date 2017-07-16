# builds lombardi aggregate tables

# qbs
psql -d nfldb -f qb_stats.sql
psql -d nfldb -f qb_aggs.sql

# defense
psql -d nfldb -f def_stats.sql
psql -d nfldb -f def_games.sql
psql -d nfldb -f def_aggs.sql
