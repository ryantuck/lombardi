create table if not exists bucket_results (
    player text,
    position text,
    metric text,
    week integer,
    yards integer,
    sample text,
    prob_yds float,
    bucket_size integer,
    primary key (
        player,
        position,
        metric,
        bucket_size,
        week
    )
);
