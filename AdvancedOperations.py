import pandas as pd
people_data=pd.read_csv('/Users/bhoomi/Documents/IMDBdataset/people.tsv',sep='\t',na_values=["\\N", ""],low_memory=True)
title_alternates_data=pd.read_csv('/Users/bhoomi/Documents/IMDBdataset/title_alternates.tsv',sep='\t',na_values=["\\N", ""],low_memory=True)
title_episode_data=pd.read_csv('/Users/bhoomi/Documents/IMDBdataset/title_episode.tsv',sep='\t',na_values=["\\N", ""],low_memory=True)
title_crew_data=pd.read_csv('/Users/bhoomi/Documents/IMDBdataset/title_crew.tsv',sep='\t',na_values=["\\N", ""],low_memory=True)
title_principals_data=pd.read_csv('/Users/bhoomi/Documents/IMDBdataset/title_principals.tsv',sep='\t',na_values=["\\N", ""],low_memory=True)
title_ratings_data=pd.read_csv('/Users/bhoomi/Documents/IMDBdataset/title_ratings.tsv',sep='\t',na_values=["\\N", ""],low_memory=True)
titles_data=pd.read_csv('/Users/bhoomi/Documents/IMDBdataset/titles.tsv',sep='\t',na_values=["\\N", ""],low_memory=True)

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