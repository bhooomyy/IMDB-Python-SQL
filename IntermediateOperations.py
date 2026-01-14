import pandas as pd
people_data=pd.read_csv('/Users/bhoomi/Documents/IMDBdataset/people.tsv',sep='\t',na_values=["\\N", ""],low_memory=True)
title_alternates_data=pd.read_csv('/Users/bhoomi/Documents/IMDBdataset/title_alternates.tsv',sep='\t',na_values=["\\N", ""],low_memory=True)
title_episode_data=pd.read_csv('/Users/bhoomi/Documents/IMDBdataset/title_episode.tsv',sep='\t',na_values=["\\N", ""],low_memory=True)
title_crew_data=pd.read_csv('/Users/bhoomi/Documents/IMDBdataset/title_crew.tsv',sep='\t',na_values=["\\N", ""],low_memory=True)
title_principals_data=pd.read_csv('/Users/bhoomi/Documents/IMDBdataset/title_principals.tsv',sep='\t',na_values=["\\N", ""],low_memory=True)
title_ratings_data=pd.read_csv('/Users/bhoomi/Documents/IMDBdataset/title_ratings.tsv',sep='\t',na_values=["\\N", ""],low_memory=True)
titles_data=pd.read_csv('/Users/bhoomi/Documents/IMDBdataset/titles.tsv',sep='\t',na_values=["\\N", ""],low_memory=True)


# Intermediate
# List the top 10 titles per decade (for each titleType) ranked by averageRating, breaking ties by numVotes.
titles_leftJoin_titleRatings=pd.merge(titles_data[['tconst','titleType','primaryTitle','startYear']],title_ratings_data[['tconst','averageRating','numVotes']],on='tconst',how='inner')
#print(titles_leftJoin_titleRatings.head(60))
titles_leftJoin_titleRatings['decade']=(titles_leftJoin_titleRatings['startYear']//10)*10
titles_leftJoin_titleRatings = titles_leftJoin_titleRatings.sort_values(
    by=['decade', 'titleType', 'averageRating', 'numVotes'],
    ascending=[True, True, False, False]
)
titles_leftJoin_titleRatings['rank']=titles_leftJoin_titleRatings.groupby(['decade','titleType']).cumcount()+1
top_10_titles=titles_leftJoin_titleRatings[titles_leftJoin_titleRatings['rank']<=10]
print(top_10_titles[['titleType','primaryTitle','startYear','decade','rank','averageRating','numVotes']].sort_values(['decade','titleType','rank']).head(60))




#Find the top 100 movies or TV series that are available under the highest number of different regional or language-specific titles.
movie_tvshows_filter=titles_data[(titles_data['titleType']=='movie') | (titles_data['titleType']=='tvSeries')]
titles_merge_alternates=pd.merge(movie_tvshows_filter[['tconst','titleType','primaryTitle']],title_alternates_data[['titleId','title','region','language','isOriginalTitle']],left_on='tconst',right_on='titleId',how='left')
groupby_title=titles_merge_alternates.groupby(['tconst','titleType','primaryTitle']).agg(num_region=('region','nunique'),num_language=('language','nunique'),num_alt_titles=('titleId','count'),original_title_cnt=('isOriginalTitle','max'))
result_2=groupby_title.sort_values(by=['num_region','num_language','num_alt_titles'],ascending=[False,False,False]).head(100)
print(result_2)



#Find the most common and most successful actor–director pairings.
actor_actress_filter_3=title_principals_data[(title_principals_data['category']=='actor') | (title_principals_data['category']=='actress')][['tconst','nconst']]
director_split=(title_crew_data[['tconst','directors']].dropna().assign(director=lambda df: df['directors'].str.split(',')).explode('director')[['tconst','director']])
actor_director_pair=pd.merge(director_split,actor_actress_filter_3,on='tconst',how='inner')
pair_join_ratings=actor_director_pair.merge(title_ratings_data[['tconst','averageRating','numVotes']],on='tconst',how='inner')
#result=pair_join_ratings.groupby(['director','tconst']).agg(num_movies_together=('tconst','nunique'),rating_median=('averageRating','median'),votes_median=('numVotes','median'))
#print(result.sort_values(by=['num_movies_together','rating_median','votes_median'],ascending=[False,False,False]).head(100))
tmp=pair_join_ratings.copy()
tmp['rating_x_votes']=tmp['averageRating']*tmp['numVotes']
result=tmp.groupby(['director','nconst']).agg(
    num_movie_cnt=('tconst','nunique'),
    total_votes=('numVotes','sum'),
    rating_x_votes=('rating_x_votes','sum'))
result['weighted_rating']=result['rating_x_votes']/result['total_votes']
top_100=result.sort_values(by=['weighted_rating','num_movie_cnt','total_votes'],ascending=[False,False,False]).head(100)
print(top_100)