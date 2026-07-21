-- This test checks if the string 'min' still exists anywhere in the column.
-- We cast the column to text just to perform the search. If it returns rows, the test fails.

select
    show_id,
    duration_minutes
from {{ ref('int_netflix_titles') }}
where cast(duration_minutes as text) like '%min%'