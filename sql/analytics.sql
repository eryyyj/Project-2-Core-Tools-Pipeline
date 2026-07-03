-- 1. The Content Boom (Year-over-Year Growth)
-- Calculates how many titles Netflix added each year, and compares it to the previous year's total to see if their acquisition rate is growing or shrinking.
WITH YearlyCounts AS (
    SELECT 
        EXTRACT(YEAR FROM date_added) AS added_year,
        COUNT(*) AS total_titles
    FROM staging_clean
    WHERE date_added IS NOT NULL
    GROUP BY EXTRACT(YEAR FROM date_added)
)
SELECT 
    added_year,
    total_titles,
    LAG(total_titles) OVER (ORDER BY added_year) AS prev_year_titles,
    total_titles - LAG(total_titles) OVER (ORDER BY added_year) AS yoy_difference
FROM YearlyCounts
ORDER BY added_year;

-- 2. Regional Top Directors (Ranking)
-- Ranks directors based on how many titles they have produced, partitioned by country.
WITH DirectorCounts AS (
    SELECT 
        country,
        director,
        COUNT(*) AS title_count
    FROM staging_clean
    WHERE director IS NOT NULL AND country IS NOT NULL
    GROUP BY country, director
),
RankedDirectors AS (
    -- We calculate the rank in this second CTE
    SELECT 
        country,
        director,
        title_count,
        RANK() OVER (PARTITION BY country ORDER BY title_count DESC) AS regional_rank
    FROM DirectorCounts
)
SELECT 
    country,
    director,
    title_count
FROM RankedDirectors
WHERE regional_rank = 1
ORDER BY country;

-- 3. The Content Strategy Shift (Movies vs. TV Shows)
-- Analyzes the ratio of Movies to TV Shows released each year over the last decade.
SELECT 
    release_year,
    type,
    COUNT(*) AS total_releases
FROM staging_clean
WHERE release_year >= 2010
GROUP BY release_year, type
ORDER BY release_year DESC, type;

-- 4. The "Twin Releases" (Self-Join)
-- Finds directors who released more than one piece of content on Netflix in the exact same year.
SELECT 
    t1.director,
    t1.release_year,
    t1.title AS title_1,
    t2.title AS title_2
FROM staging_clean t1
JOIN staging_clean t2 
    ON t1.director = t2.director 
    AND t1.release_year = t2.release_year
    -- Ensure we don't match the movie to itself, and avoid duplicate pairings
    AND t1.show_id < t2.show_id 
WHERE t1.director IS NOT NULL
ORDER BY t1.director, t1.release_year DESC;

-- 5. The Longest Movies per Age Rating
-- Finds the single longest movie for each rating category (PG-13, TV-MA, R, etc.).WITH MovieDurations AS (
WITH MovieDurations AS (
    SELECT 
        rating,
        title,
        -- Splits "90 min" by the space, grabs the first part ("90"), and turns it into an integer
        CAST(SPLIT_PART(duration, ' ', 1) AS INTEGER) AS duration_minutes
    FROM staging_clean
    WHERE type = 'Movie' 
      AND duration LIKE '% min'
      AND rating IS NOT NULL
),
RankedMovies AS (
    SELECT 
        rating,
        title,
        duration_minutes,
        ROW_NUMBER() OVER (PARTITION BY rating ORDER BY duration_minutes DESC) as rank
    FROM MovieDurations
)
SELECT 
    rating,
    title,
    duration_minutes
FROM RankedMovies
WHERE rank = 1
ORDER BY duration_minutes DESC;