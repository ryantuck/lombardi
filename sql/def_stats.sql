drop table if exists lombardi.def_stats;

create table lombardi.def_stats as

select
    case
        when team = home_team then away_team
        when team = away_team then home_team
        else null
        end as defense,
    year,
    week,
    team as opp,
    yards,
    touchdowns,
    interceptions,
    attempts,
    completions
from
    lombardi.qb_stats
;
