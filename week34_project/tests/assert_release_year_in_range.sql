select
    show_id,
    release_year
from {{ ref('int_netflix_titles') }}
where release_year < 1925 or release_year > 2026