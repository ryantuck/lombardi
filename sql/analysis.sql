select
    position,
--    player,
--    bucket_size,
    better_prob,
    count(*)
from (
    select
        r.position,
        r.player,
        r.week,
        r.bucket_size,
        case
            when r.prob_yds > c.prob_yds then 'running'
            else 'cumulative'
        end as better_prob
    from (
        select
            position,
            player,
            week,
            bucket_size,
            prob_yds
        from
            bucket_results
        where
            sample = 'cumulative'
        ) c
        inner join (
            select
                position,
                player,
                week,
                bucket_size,
                prob_yds
            from
                bucket_results
            where
                sample = 'running'
        ) r
        on
            r.player = c.player and
            r.week = c.week and
            r.bucket_size = c.bucket_size
) x
group by
    position,
--    player,
--    bucket_size,
    better_prob
order by
    position
--    player,
--    bucket_size
