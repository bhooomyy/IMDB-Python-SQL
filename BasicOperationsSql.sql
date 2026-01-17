use imdb ;
-- List the first 50 movies released between 2010 and 2015
select * from titles where titleType='movie' and (startYear>=2010 and startYear<=2015);

-- Count how many titles exist for each title type and display the results in descending order.
select titleType,count(*) as cnt from titles group by titleType order by cnt desc;

-- Find the top 20 highest-rated titles that have received at least 50,000 votes.
select t.primaryTitle,t.titleType,r.averageRating,r.numVotes from titles t left join title_rating r on t.tconst=r.tconst where r.numVotes>=50000 order by r.averageRating desc limit 20;
