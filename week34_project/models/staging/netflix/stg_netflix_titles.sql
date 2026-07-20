{{ config(materialized = 'view')}}

with raw_data as (
    select * from {{source('raw_data', 'staging_raw')}} -- getting the data from the database
),

deduplicated_and_filtered as (
    select *,
    row_number() over (partition by show_id order by show_id) as row_num -- creating row number for every bucket of show_id
    from raw_data
    where title is not null -- this drops any shows or movies without titles
),

cleaned as (
    select
        coalesce(trim(show_id), 'Unknown') as show_id, -- this fixes the value string of the column and replaces null values with unknown
        coalesce(initcap('type'), 'Unknown') as show_type, -- this transforms the value string of the column into title case and replaces null values with unknown

        initcap(trim(title)) as show_title, -- transforms the value string to tile case

        -- this fixes the value string of the column and replaces null values with unknown
        coalesce(trim(director),'Unknown') as director, 
        coalesce(trim('cast'), 'Unknown') as casts,
        coalesce(trim(country), 'Unknown') as country,
        coalesce(trim(rating), 'Unknown') as rating,
        coalesce(trim(duration), 'Unknown') as duration,

        -- fixes the datatype of these columns
        cast(date_added as date) as date_added,
        cast(release_year as integer) as release_year

    from deduplicated_and_filtered
    where row_num = 1 -- this condition drops the duplicates
)

select * from cleaned

order by cast(regexp_replace(show_id, '[^0-9]', '', 'g') as integer) -- orders the show_id and deletes any string characters into it