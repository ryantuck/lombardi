-- regular season template
select
    g.week,
    sum(pp.rushing_yds) as yards
from
    play_player pp
    join
        game g using (gsis_id)
    join
        player p using (player_id)
where
    g.season_year = {{ year }} and
    g.season_type = 'Regular' and
    p.full_name = '{{ full_name }}'
group by
    week
