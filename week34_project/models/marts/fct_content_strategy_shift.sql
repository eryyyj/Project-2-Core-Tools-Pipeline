{{config(materialized='table')}}

with netflix_titles as (
    select * from {{ref('int_netflix_titles')}}
),

content_strategy_shift as (
    SELECT 
        release_year,
        show_type,
        COUNT(*) AS total_releases
    FROM netflix_titles
    WHERE release_year >= 2010
    GROUP BY release_year, show_type
)

select * from content_strategy_shift
ORDER BY release_year DESC, show_type