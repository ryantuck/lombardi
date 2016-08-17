-- regular season template
select
    g.week,
    g.season_year as year,
    sum(pp.passing_yds) as yards
from
    play_player pp
    join
        game g using (gsis_id)
    join
        player p using (player_id)
where
    g.season_year > 2010 and
    g.season_type = 'Regular' and
    p.full_name = '{{ full_name }}'
group by
    week,
    year
