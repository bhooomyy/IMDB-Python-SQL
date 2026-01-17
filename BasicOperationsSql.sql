use imdb ;
-- List the first 50 movies released between 2010 and 2015
select * from titles where titleType='movie' and (startYear>=2010 and startYear<=2015);

-- Count how many titles exist for each title type and display the results in descending order.
select titleType,count(*) as cnt from titles group by titleType order by cnt desc;

-- Find the top 20 highest-rated titles that have received at least 50,000 votes.
select t.primaryTitle,t.titleType,r.averageRating,r.numVotes from titles t left join title_rating r on t.tconst=r.tconst where r.numVotes>=50000 order by r.averageRating desc limit 20;

-- Identify titles that do not have any rating information available.
select t.tconst, t.primaryTitle from titles t where not exists (select 1 from title_rating r where r.tconst = t.tconst);

-- For each TV series, calculate the total number of episodes and list the top 20 series with the most episodes.
with t1 as(select parentTconst,count(*) as num_episodes from title_episode group by parentTconst)
select t.tconst,t.primaryTitle,t1.num_episodes from titles t join t1 on t.tconst=t1.parentTconst where t.titleType='tvSeries' order by t1.num_episodes desc limit 20;

-- List the top 20 people who have appeared in the highest number of titles as an actor or actress.
select p.nconst,pe.primaryName,count(distinct p.tconst) as num_titles from title_principal p join people pe on pe.nconst = p.nconst where p.category in ('actor','actress') group by p.nconst, pe.primaryName order by num_titles desc limit 20;
