{{config(materialized='table')}}


with netflix_titles as (
    select * from {{ ref('int_netflix_titles')}}
), 
-- 1. The Content Boom (Year-over-Year Growth)
-- this query calculates how many titles Netflix added each year, and compares it to the previous year's total to see if their acquisition rate is growing or shrinking.
yearly_counts AS (
    SELECT 
        EXTRACT(YEAR FROM date_added) AS added_year,
        COUNT(*) AS total_titles
    FROM netflix_titles
    WHERE date_added IS NOT NULL
    GROUP BY EXTRACT(YEAR FROM date_added)
),

content_boom_yoy as (
    SELECT 
        added_year,
        total_titles,
        LAG(total_titles) OVER (ORDER BY added_year) AS prev_year_titles,
        total_titles - LAG(total_titles) OVER (ORDER BY added_year) AS yoy_difference
    FROM yearly_counts   
)

select * from content_boom_yoy

order by added_year