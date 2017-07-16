drop table if exists lombardi.wr_aggs;

create table lombardi.wr_aggs as

select
    year,
    name,

    round(avg(yards), 2) as avg_yds,
    round(avg(touchdowns), 2) as avg_tds,
    round(avg(receptions), 2) as avg_rec,

    round(stddev(yards), 2) as std_yds,
    round(stddev(touchdowns), 2) as std_tds,
    round(stddev(receptions), 2) as std_rec,

    count(*) as num_games
from
    lombardi.wr_stats
group by
    year,
    name
order by
    year,
    name
;
