drop table if exists lombardi.def_wr_games;

create table lombardi.def_wr_games as

select
    name,
    year,
    week,
    opp,
    sum(yards) as yards,
    sum(touchdowns) as touchdowns,
    sum(receptions) as receptions,

    count(*) as num_opp_players
from
    lombardi.def_wr_stats
group by
    1,2,3,4
order by
    year,
    week
;
