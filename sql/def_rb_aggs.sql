drop table if exists lombardi.def_rb_aggs;

create table lombardi.def_rb_aggs as

select
    year,
    name,

    round(avg(yards), 2) as avg_yds,
    round(avg(touchdowns), 2) as avg_tds,
    round(avg(attempts), 2) as avg_att,

    round(stddev(yards), 2) as std_yds,
    round(stddev(touchdowns), 2) as std_tds,
    round(stddev(attempts), 2) as std_att,

    count(*) as num_games
from
    lombardi.def_rb_games
group by
    year,
    name
order by
    year,
    name
;
