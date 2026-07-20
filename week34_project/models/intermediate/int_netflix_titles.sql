{{ config(materialized = 'view')}}


with staged_data as (
    select * from {{ ref('stg_netflix_titles')}}
),

movie_duration as (
    select  
        show_id,
        show_type,
        show_title,
        director,
        casts,
        country,
        rating,
        date_added,
        release_year,
        cast(split_part(duration, ' ', 1) as integer) as duration_minutes
    from staged_data
    where show_type = 'Movies'
        and duration like '% min'
        and rating != 'Unknown'
)

select * from movie_duration