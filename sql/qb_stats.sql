drop table if exists lombardi.qb_stats;

create table lombardi.qb_stats as

select
    g.season_year as year,
    g.week,
    p.full_name as name,
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
    p.position = 'QB' and
    pp.passing_att > 0
group by
    g.week,
    g.season_year,
    p.full_name
order by
    year,
    week,
    full_name
;
