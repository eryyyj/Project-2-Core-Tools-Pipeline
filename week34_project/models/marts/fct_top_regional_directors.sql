{{config(materialized='table')}}

with netflix_titles as (
    select * from {{ref('int_netflix_titles')}}
),

director_counts as (
    SELECT 
        country,
        director,
        COUNT(*) AS title_count
    FROM netflix_titles
    WHERE director IS NOT NULL AND country IS NOT NULL
    GROUP BY country, director
),
ranked_directors AS (
    SELECT 
        country,
        director,
        title_count,
        RANK() OVER (PARTITION BY country ORDER BY title_count DESC) AS regional_rank
    FROM director_counts
),
top_regional_directors as (
    SELECT 
        country,
        director,
        title_count
    FROM ranked_directors
    WHERE regional_rank = 1
)

select * from top_regional_directors
ORDER BY country