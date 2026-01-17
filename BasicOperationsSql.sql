use imdb ;
-- List the first 50 movies released between 2010 and 2015
select * from titles where titleType='movie' and (startYear>=2010 and startYear<=2015);

-- Count how many titles exist for each title type and display the results in descending order.
select titleType,count(*) as cnt from titles group by titleType order by cnt desc;