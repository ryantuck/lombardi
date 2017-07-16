drop table if exists lombardi.qb_stats;

create table lombardi.qb_stats as

select
    g.season_year as year,
    g.week,
    p.full_name as name,
    pp.team,
    g.home_team,
    g.away_team,
    sum(pp.passing_yds) as yards,
    sum(pp.passing_tds) as touchdowns,
    sum(pp.passing_int) as interceptions,
    sum(pp.passing_att) as attempts,
    sum(pp.passing_cmp) as completions
from
    play_player pp
    join
        game g using (gsis_id)
    join
        player p using (player_id)
where
    g.season_type = 'Regular' and
    pp.passing_att > 0
group by
    1,2,3,4,5,6
order by
    1,2,3
;
