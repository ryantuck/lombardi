drop table if exists lombardi.qb_aggs;

create table lombardi.qb_aggs as

select
    year,
    name,

    round(avg(yards), 2) as avg_yds,
    round(avg(touchdowns), 2) as avg_tds,
    round(avg(interceptions), 2) as avg_int,
    round(avg(completions), 2) as avg_cmp,
    round(avg(attempts), 2) as avg_att,

    round(stddev(yards), 2) as std_yds,
    round(stddev(touchdowns), 2) as std_tds,
    round(stddev(interceptions), 2) as std_int,
    round(stddev(completions), 2) as std_cmp,
    round(stddev(attempts), 2) as std_att,

    count(*) as num_games
from
    lombardi.qb_stats
group by
    year,
    name
order by
    year,
    name
;
