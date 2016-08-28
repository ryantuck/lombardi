create table if not exists gamma_results (
    player text,
    position text,
    metric text,
    week integer,
    yards integer,
    sample text,
    shape float,
    scale float,
    primary key (
        player,
        position,
        metric,
        sample,
        week
    )
);
