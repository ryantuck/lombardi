drop table if exists lombardi.qb_aggs;

create table lombardi.qb_aggs as

select
    year,
    full_name,
    round(avg(yards), 2) as avg_yds,
    round(avg(touchdowns), 2) as avg_tds,
    round(avg(interceptions), 2) as avg_int,
    round(avg(completions), 2) as avg_cmp,
    round(avg(attempts), 2) as avg_att,
    count(*) as num_games
from
    lombardi.qb_stats
group by
    year,
    full_name
order by
    year,
    full_name
;
