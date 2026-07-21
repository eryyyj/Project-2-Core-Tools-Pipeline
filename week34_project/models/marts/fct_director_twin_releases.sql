{{config(materialized='table')}}

with netflix_titles as (
    select * from {{ref('int_netflix_titles')}}
),

director_twin_releases as (
    SELECT 
        t1.director,
        t1.release_year,
        t1.show_title AS title_1,
        t2.show_title AS title_2
    FROM netflix_titles t1
    JOIN netflix_titles t2 
        ON t1.director = t2.director 
        AND t1.release_year = t2.release_year
        -- Ensure we don't match the movie to itself, and avoid duplicate pairings
        AND t1.show_id < t2.show_id 
    WHERE t1.director != 'Unknown'
)

select * from director_twin_releases
ORDER BY director, release_year DESC