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