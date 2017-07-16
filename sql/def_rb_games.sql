drop table if exists lombardi.def_rb_games;

create table lombardi.def_rb_games as

select
    name,
    year,
    week,
    opp,
    sum(yards) as yards,
    sum(touchdowns) as touchdowns,
    sum(attempts) as attempts,

    count(*) as num_opp_players
from
    lombardi.def_rb_stats
group by
    1,2,3,4
order by
    year,
    week
;
