-- This test verifies that every value in the column is a whole integer.
-- If any value has a decimal component (e.g., 90.5), the test fails.

select
    show_id,
    duration_minutes
from {{ ref('int_netflix_titles') }}
where floor(duration_minutes) != duration_minutes