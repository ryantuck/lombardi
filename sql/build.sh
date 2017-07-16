# builds lombardi aggregate tables

# qbs
psql -d nfldb -f qb_stats.sql
psql -d nfldb -f qb_aggs.sql

# defense
psql -d nfldb -f def_stats.sql
psql -d nfldb -f def_games.sql
psql -d nfldb -f def_aggs.sql

# rbs
psql -d nfldb -f rb_stats.sql
psql -d nfldb -f rb_aggs.sql

# wrs
psql -d nfldb -f wr_stats.sql
psql -d nfldb -f wr_aggs.sql
