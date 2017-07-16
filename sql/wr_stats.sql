drop table if exists lombardi.wr_stats;

create table lombardi.wr_stats as

select
    g.season_year as year,
    g.week,
    p.full_name as name,
    pp.team,
    g.home_team,
    g.away_team,
    sum(pp.receiving_yds) as yards,
    sum(pp.receiving_tds) as touchdowns,
    sum(pp.receiving_rec) as receptions
from
    play_player pp
    join
        game g using (gsis_id)
    join
        player p using (player_id)
where
    g.season_type = 'Regular' and
    pp.receiving_rec > 0
group by
    1,2,3,4,5,6
order by
    1,2,3
;
