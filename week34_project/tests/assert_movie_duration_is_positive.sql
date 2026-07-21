-- This test ensures that the transformation didn't create any impossible 0 or negative minute movies.
-- If this query returns any records, the test fails.

select
    show_id,
    duration_minutes
from {{ ref('int_netflix_titles') }} -- Looks at your intermediate model
where duration_minutes <= 0