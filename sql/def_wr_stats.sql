drop table if exists lombardi.def_wr_stats;

create table lombardi.def_wr_stats as

select
    case
        when team = home_team then away_team
        when team = away_team then home_team
        else null
        end as name,
    year,
    week,
    team as opp,
    yards,
    touchdowns,
    receptions
from
    lombardi.wr_stats
;
