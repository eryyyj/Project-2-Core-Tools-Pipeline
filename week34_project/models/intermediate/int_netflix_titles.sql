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
        
        -- Extract minutes for Movies only
        case 
            when show_type = 'Movie' and duration like '% min' 
                then cast(split_part(duration, ' ', 1) as integer)
            else null 
        end as duration_minutes,

        -- Extract seasons for TV Shows only
        case 
            when show_type = 'TV Show' and duration like '%Season%' 
                then cast(split_part(duration, ' ', 1) as integer)
            else null 
        end as duration_seasons

    from {{ ref('stg_netflix_titles') }}
    where rating != 'Unknown'
)

select * from movie_duration