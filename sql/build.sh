# builds lombardi aggregate tables

# qbs
psql -d nfldb -f qb_stats.sql
psql -d nfldb -f qb_aggs.sql

# rbs
psql -d nfldb -f rb_stats.sql
psql -d nfldb -f rb_aggs.sql

# wrs
psql -d nfldb -f wr_stats.sql
psql -d nfldb -f wr_aggs.sql

# defense
psql -d nfldb -f def_qb_stats.sql
psql -d nfldb -f def_qb_games.sql
psql -d nfldb -f def_qb_aggs.sql

psql -d nfldb -f def_rb_stats.sql
psql -d nfldb -f def_rb_games.sql
psql -d nfldb -f def_rb_aggs.sql

psql -d nfldb -f def_wr_stats.sql
psql -d nfldb -f def_wr_games.sql
psql -d nfldb -f def_wr_aggs.sql
