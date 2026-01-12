from cleaning import people_data,title_alternates_data,title_crew_data,title_episode_data,title_principals_data,title_ratings_data,titles_data
import pandas as pd
####### Analysis #########
#List the first 50 movies released between 2010 and 2015
titleType_movies=titles_data[titles_data['titleType']=='movie']
#print(titleType_movies.head())
titleType_movies_2010_2015=titleType_movies[titleType_movies['startYear'].between(2010,2015)].sort_values(by=['startYear'])
print(titleType_movies_2010_2015[['tconst','primaryTitle','startYear']].head(50))



#Count how many titles exist for each title type and display the results in descending order.
cnt_title_titleType=titles_data.groupby(['titleType']).size().reset_index(name='cnt_title_titleType')
cnt_title_titleType=cnt_title_titleType.sort_values(by='cnt_title_titleType',ascending=False)
print(cnt_title_titleType)



#Find the top 20 highest-rated titles that have received at least 50,000 votes.
tconst_50000_votes=title_ratings_data[title_ratings_data['numVotes']>=50000].sort_values(by='averageRating',ascending=False)
#print(tconst_50000_votes)
top_20_movies=pd.merge(titles_data[['tconst','titleType','primaryTitle']],tconst_50000_votes[['tconst','averageRating','numVotes']],on='tconst',how='inner')
print(top_20_movies.head(20))



#Identify titles that do not have any rating information available.
'''empty=title_ratings_data['averageRating'].isna().any().sum()
print(empty) '''
#Identify titles that do not have any rating information available.
title_leftJoin_title_ratings=pd.merge(titles_data[['tconst','titleType','primaryTitle']],title_ratings_data[['tconst','averageRating']],on='tconst',how='left')
null_title=title_leftJoin_title_ratings[title_leftJoin_title_ratings['averageRating'].isna()]
print(null_title[['tconst','primaryTitle','averageRating']])