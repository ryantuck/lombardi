drop table if exists lombardi.def_games;

create table lombardi.def_games as

select
    name,
    year,
    week,
    opp,
    sum(yards) as yards,
    sum(touchdowns) as touchdowns,
    sum(interceptions) as interceptions,
    sum(attempts) as attempts,
    sum(completions) as completions,

    count(*) as num_qbs
from
    lombardi.def_stats
group by
    1,2,3,4
order by
    year,
    week
;
