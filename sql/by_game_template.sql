-- regular season template
select
    g.week,
    g.season_year as year,
    sum(pp.{{ metric }}) as {{ metric }}
from
    play_player pp
    join
        game g using (gsis_id)
    join
        player p using (player_id)
where
    {% if min_year is not none %}
    g.season_year >= {{ min_year }} and
    {% endif %}
    {% if max_year is not none %}
    g.season_year <= {{ max_year }} and
    {% endif %}
    g.season_type = 'Regular' and
    p.full_name = '{{ player }}'
group by
    week,
    year
