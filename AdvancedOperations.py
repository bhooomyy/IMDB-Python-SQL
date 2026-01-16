import pandas as pd
from cleaning import people_data,title_alternates_data,title_crew_data,title_episode_data,title_principals_data,title_ratings_data,titles_data

#Identify, for each actor or actress, the first movie or TV title or any titleType where their popularity significantly increased compared to their previous work.
#For each actor or actress, find the earliest title where the number of votes is at least three times higher than their recent average and the rating is not worse than their prior work.
actor_actress_filter_adv=title_principals_data[(title_principals_data['category']=='actor')|(title_principals_data['category']=='actress')]
titles_data=titles_data[['tconst','primaryTitle','startYear']].dropna(subset=['startYear'])
merge_title=actor_actress_filter_adv.merge(titles_data[['tconst','startYear','primaryTitle']],on='tconst',how='inner')
merge_ratings=merge_title.merge(title_ratings_data,on='tconst',how='inner').sort_values(by=['nconst','startYear'],ascending=True)

merge_ratings['baseline_rating']=(merge_ratings.groupby('nconst')['averageRating'].transform(lambda s: s.rolling(5,min_periods=5).mean().shift(1)))
merge_ratings['baseline_votes']=(merge_ratings.groupby('nconst')['numVotes'].transform(lambda s: s.rolling(5,min_periods=5).mean().shift(1)))

breakouts=merge_ratings[merge_ratings['baseline_votes'].notna()&merge_ratings['baseline_rating'].notna()&(merge_ratings['numVotes']>=3*merge_ratings['baseline_votes'])&(merge_ratings['averageRating']>=merge_ratings['baseline_rating'])]
first_breakout=breakouts.sort_values(by=['nconst','startYear']).groupby('nconst').first()
print(first_breakout[['nconst','startYear','primaryTitle','averageRating','numVotes','baseline_rating','baseline_votes']].head(50))





# Detect TV series with broken episode continuity (duplicates, gaps, missing episode numbers) and rank the top 50 series by anomaly severity.
tvseries_filter=titles_data[titles_data['titleType']=='tvSeries']
title_join_episode=tvseries_filter.merge(title_episode_data,left_on='tconst',right_on='parentTconst',how='inner').sort_values(by=['seasonNumber','episodeNumber'],ascending=[True,True])
#result_2_adv=title_join_episode[(title_join_episode['seasonNumber'].isna()) | (title_join_episode['episodeNumber'].isna()) | (title_join_episode['seasonNumber'].isna()) | (title_join_episode['episodeNumber']==0.0)]
def missing_eps(s):
    invalid=s[s.isna() | s<=0.0].tolist()
    valid=s.dropna()
    valid=valid[valid>0].astype(int)
    if valid.empty:
        return invalid
    expected=set(range(valid.min(),valid.max()+1))
    missing=sorted(expected-set(valid))
    return missing+invalid
missing_episodes=title_join_episode.groupby(['parentTconst','primaryTitle','seasonNumber'])['episodeNumber'].apply(missing_eps).reset_index(name='missing_episode')
anomaly=missing_episodes[missing_episodes['missing_episode'].str.len()>0]
print(anomaly.head(50))





# Identify titles where at least one person is credited as both a writer and a director, then measure how common and how successful these titles are by content type and genre.
genre_split=titles_data[['tconst','titleType','genres']].dropna(subset=['genres']).assign(genre=lambda df:df['genres'].str.split(',')).explode('genre')[['tconst','titleType','genre']]
director_split=title_crew_data[['tconst','directors']].dropna().assign(director=lambda df:df['directors'].str.split(',')).explode('director')[['tconst','director']]
writer_split=title_crew_data[['tconst','writers']].dropna().assign(writer=lambda df:df['writers'].str.split(',')).explode('writer')[['tconst','writer']]

director_writer_overlap=director_split.merge(writer_split,left_on=['tconst','director'],right_on=['tconst','writer'],how='inner')

single_auth=director_writer_overlap['tconst'].dropna().unique()
title_meta=genre_split.copy()
title_meta['is_single_auth']=title_meta['tconst'].isin(single_auth)

how_common=title_meta.groupby(['titleType','genre']).agg(
    total_title=('tconst','nunique'),
    is_single_auth_cnt=('is_single_auth','sum')
)
how_common['single_auth_rate']=how_common['is_single_auth_cnt']/how_common['total_title']

title_meta_merge_rating=title_meta.merge(title_ratings_data,on=['tconst'],how='left')
title_meta_merge_rating['rating_x_votes']=title_meta_merge_rating['averageRating']*title_meta_merge_rating['numVotes']
success=title_meta_merge_rating.groupby(['titleType','genre','is_single_auth']).agg(
    total_titles=('tconst','nunique'),
    total_votes=('numVotes','sum'),
    total_rating_x_votes=('rating_x_votes','sum')
)
success['weighted_rating']=success['total_rating_x_votes']/success['total_votes'].replace(0, pd.NA)
how_common = how_common.reset_index()
success = success.reset_index()

print("\n=== Single-Author Prevalence by Title Type & Genre ===\n",how_common.sort_values(['single_auth_rate','total_title'], ascending=[False, False]).head(20))
print("\n=== Single-Author Titles (Writer = Director) ===\n",success[success['is_single_auth']].sort_values(['weighted_rating','total_votes'], ascending=[False, False]).head(20))
print("\n=== Non-Single-Author Titles (Writer ≠ Director) ===\n",success[~success['is_single_auth']].sort_values(['weighted_rating','total_votes'], ascending=[False, False]).head(20))






'''For each decade, find which genres were most popular and how their popularity increased or decreased compared to the previous decade, 
using audience votes and ratings.'''
titles_data['decade']=(titles_data['startYear']//10)*10
genres_split=titles_data[['tconst','titleType','primaryTitle','genres','startYear','decade']].dropna(subset=['genres']).assign(genre=lambda df:df['genres'].str.split(',')).explode('genre')[['tconst','titleType','primaryTitle','genre','startYear','decade']]

genre_merge_ratings=pd.merge(genres_split[['tconst','titleType','primaryTitle','genre','startYear','decade']],title_ratings_data[['tconst','averageRating','numVotes']],on='tconst',how='inner')
genre_merge_ratings['rating_x_votes']=genre_merge_ratings['averageRating']*genre_merge_ratings['numVotes']

result=genre_merge_ratings.groupby(['decade','genre','titleType']).agg(
    total_title=('tconst','nunique'),
    total_votes=('numVotes','sum'),
    rating_x_votes_sum=('rating_x_votes','sum')
)
result['decade_total_vote']=result.groupby(['decade','titleType'])['total_votes'].transform('sum')
result['vote_share']=result['total_votes']/result['decade_total_vote']
print(result.sort_values(by=['decade','vote_share'],ascending=[True,False]).head(60))







# Find the top 100 actors/actresses ranked by total audience votes across all titles they appeared in, and show their vote-weighted average rating.
# For each actor/actress, find their top 3 genres by total votes, and label them as “specialist” (one genre dominates) or “crossover” (votes spread across genres).
actor_actress_filter=title_principals_data[(title_principals_data['category']=='actor')|(title_principals_data['category']=='actress')]
actor_actress_filter=actor_actress_filter.merge(people_data[['nconst','primaryName']],on='nconst',how='left')
actor_merger_rating=actor_actress_filter[['tconst','nconst','primaryName','category']].merge(title_ratings_data,on='tconst',how='inner')
actor_merger_rating = actor_merger_rating.drop_duplicates(subset=['tconst','nconst'])
actor_merger_rating['rating_x_votes']=actor_merger_rating['averageRating']*actor_merger_rating['numVotes']
result_1=actor_merger_rating.groupby(['nconst','primaryName']).agg(
    total_titles=('tconst','nunique'),
    total_votes=('numVotes','sum'),
    total_rating_x_votes=('rating_x_votes','sum')
)
result_1['weighted_rating']=result_1['total_rating_x_votes']/result_1['total_votes']
#print('##### result_1 #####')
#print(result_1.sort_values(by=['total_votes','weighted_rating'],ascending=[False,False]).head(100))
#print('##### result_2 #####')
genres_split=titles_data[['tconst','titleType','primaryTitle','genres']].dropna(subset=['genres']).assign(genre=lambda df:df['genres'].str.split(',')).explode('genre')[['tconst','titleType','primaryTitle','genre']]
refined_result_1=actor_merger_rating[['tconst','nconst','primaryName','numVotes']].drop_duplicates(['nconst','tconst'])
result_1_merge_genre=refined_result_1.merge(genres_split,on='tconst',how='inner').groupby(['nconst','primaryName','genre']).agg(total_votes=('numVotes','sum')).reset_index()

result_1_merge_genre=result_1_merge_genre.sort_values(['nconst', 'total_votes'],ascending=[True, False])
result_1_merge_genre['rank']=result_1_merge_genre.groupby('nconst').cumcount()+1
result_2=result_1_merge_genre[result_1_merge_genre['rank']<=3].sort_values(by=['nconst','rank','genre'])


actor_total_votes=(result_1_merge_genre.groupby('nconst').agg(actor_total_votes=('total_votes','sum')))
top_genre_votes = (result_1_merge_genre[result_1_merge_genre['rank'] == 1][['nconst', 'total_votes']].rename(columns={'total_votes': 'top_genre_votes'}))
actor_label = actor_total_votes.merge(top_genre_votes, on='nconst', how='left')
actor_label['top_genre_share'] = actor_label['top_genre_votes'] / actor_label['actor_total_votes']

SPECIALIST_THRESHOLD = 0.70
actor_label['label'] = 'crossover'
actor_label.loc[actor_label['top_genre_share'] >= SPECIALIST_THRESHOLD, 'label'] = 'specialist'
result_2 = result_2.merge(actor_label[['nconst', 'label', 'top_genre_share']], on='nconst', how='left')
print(result_2.head(50))