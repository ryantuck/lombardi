-- how many rbs played how many games
select
    *
from (
    select
        player_name,
        year,
        count(*) as games
    from (
        select
            p.full_name as player_name,
            g.week,
            g.season_year as year,
            sum(pp.rushing_yds) as rushing_yds
        from
            play_player pp
            join
                game g using (gsis_id)
            join
                player p using (player_id)
        where
            g.season_type = 'Regular' and
            p.position = 'RB'
        group by
            p.full_name,
            week,
            year
        order by
            year,
            week
    ) pbw
    where
        rushing_yds > 0
    group by
        player_name,
        year
) gc
where games >= 10
;
