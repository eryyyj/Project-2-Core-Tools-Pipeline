{{config(materialized='table')}}

with netflix_titles as (
    select * from {{ref('int_netflix_titles')}}
),

movie_durations AS (
    SELECT 
        rating,
        show_title,
        duration_minutes
    FROM netflix_titles
),
ranked_movies AS (
    SELECT 
        rating,
        show_title,
        duration_minutes,
        ROW_NUMBER() OVER (PARTITION BY rating ORDER BY duration_minutes DESC) as duration_rank
    FROM movie_durations
),
longest_movies_by_rating as (
    SELECT 
        rating,
        show_title,
        duration_minutes
    FROM ranked_movies
    WHERE duration_rank = 1
)

select * from longest_movies_by_rating
ORDER BY duration_minutes DESC