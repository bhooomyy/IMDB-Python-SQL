use imdb;
-- List the top 10 titles per decade (for each titleType) ranked by averageRating, breaking ties by numVotes.
with ranked_titles as 
(select t.titleType,FLOOR(t.startYear / 10) * 10 AS decade,t.tconst,t.primaryTitle,r.averageRating,r.numVotes, row_number() over 
(partition by t.titleType, FLOOR(t.startYear / 10) * 10 order by r.averageRating desc, r.numVotes desc) as rn 
from titles t join title_rating r on t.tconst = r.tconst where t.startYear is not null)

select titleType,decade,tconst,primaryTitle,averageRating,numVotes from ranked_titles where rn <= 10 order by titleType, decade, rn;


