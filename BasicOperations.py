from cleaning import people_data,title_alternates_data,title_crew_data,title_episode_data,title_principals_data,title_ratings_data,titles_data

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