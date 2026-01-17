use imdb;
-- List the top 10 titles per decade (for each titleType) ranked by averageRating, breaking ties by numVotes.
with ranked_titles as 
(select t.titleType,FLOOR(t.startYear / 10) * 10 AS decade,t.tconst,t.primaryTitle,r.averageRating,r.numVotes, row_number() over 
(partition by t.titleType, FLOOR(t.startYear / 10) * 10 order by r.averageRating desc, r.numVotes desc) as rn 
from titles t join title_rating r on t.tconst = r.tconst where t.startYear is not null)

select titleType,decade,tconst,primaryTitle,averageRating,numVotes from ranked_titles where rn <= 10 order by titleType, decade, rn;


-- Find the top 100 movies or TV series that are available under the highest number of different regional or language-specific titles.
select  t.tconst,t.primaryTitle,t.titleType,count(distinct ta.title) as num_alt_titles,count(distinct ta.region) as num_regions,count(distinct ta.language) as num_languages
from titles t join title_alternate ta on ta.titleId = t.tconst 
where t.titleType in ('movie','tvSeries') 
group by t.tconst, t.primaryTitle, t.titleType 
order by num_alt_titles desc, num_regions desc, num_languages desc 
limit 100;



-- Find the most common and most successful actor–director pairings.
WITH RECURSIVE nums AS (
  SELECT 1 AS n
  UNION ALL
  SELECT n + 1 FROM nums WHERE n < 10
),
director_titles AS (
  SELECT
    tc.tconst,
    TRIM(SUBSTRING_INDEX(SUBSTRING_INDEX(tc.directors, ',', nums.n), ',', -1)) AS director_nconst
  FROM title_crew tc
  JOIN nums
    ON tc.directors IS NOT NULL
   AND tc.directors <> '\\N'
   AND (CHAR_LENGTH(tc.directors) - CHAR_LENGTH(REPLACE(tc.directors, ',', '')) + 1) >= nums.n
),
pair_scores AS (
  SELECT
    dt.director_nconst,
    tp.nconst AS actor_nconst,
    COUNT(DISTINCT tp.tconst) AS num_titles_together,
    SUM(tr.numVotes) AS total_votes,
    SUM(tr.averageRating * tr.numVotes) / SUM(tr.numVotes) AS weighted_rating
  FROM director_titles dt
  JOIN title_principal tp
    ON tp.tconst = dt.tconst
  JOIN title_rating tr
    ON tr.tconst = tp.tconst
  WHERE tp.category IN ('actor','actress')
  GROUP BY dt.director_nconst, tp.nconst
  HAVING COUNT(DISTINCT tp.tconst) >= 2
),
ranked AS (
  SELECT
    *,
    ROW_NUMBER() OVER (
      ORDER BY weighted_rating DESC, num_titles_together DESC, total_votes DESC
    ) AS rn
  FROM pair_scores
)
SELECT
  director_nconst,
  actor_nconst,
  num_titles_together,
  total_votes,
  weighted_rating
FROM ranked
WHERE rn <= 100
ORDER BY rn;